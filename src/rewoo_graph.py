
import re

from langgraph.graph import END, StateGraph, START

from src.base import ReWOO
from src.nodes import Planner, Solver, Workers

class ReWOOGraph: 
    def __init__(self, config): 
        self.planner = Planner(config=config['llm'])
        self.solver  = Solver(config=config['llm'])

        self.search_engine = Workers.call_engine(name="search",
                                                 config=config['tools']['search'])
        self.llm_engine = Workers.call_engine(name="llm", 
                                              config=config['llm'])

        self.regex_pattern = r"Plan:\s*(.+)\s*(#E\d+)\s*=\s*(\w+)\s*\[([^\]]+)\]"


    def build_graph(self):
        graph = StateGraph(ReWOO)

        # Add node 
        graph.add_node("plan", self.get_plan)
        graph.add_node("tool", self.tool_execution)
        graph.add_node("solve", self.get_solve)

        # Create edges to build logics of the agent
        graph.add_edge("plan", "tool")
        graph.add_edge("solve", END)
        graph.add_conditional_edges("tool", self._route)
        graph.add_edge(START, "plan")

        app = graph.compile()

        return app

    def _route(self, state):
        _step = self._get_current_task(state)
        if _step is None:
            # We have executed all tasks
            return "solve"
        else:
            # We are still executing tasks, loop back to the "tool" node
            return "tool"
        
    def get_plan(self, state: ReWOO):
        task = state["task"]
        result = self.planner.run(task)
        # Find all matches in the sample text
        matches = re.findall(self.regex_pattern, result.content)
        return {"steps": matches, "plan_string": result.content}
    
    def get_solve(self, state: ReWOO):
        plan = ""

        for _plan, step_name, tool, tool_input in state["steps"]:
            _results = state["results"] or {}
            for k, v in _results.items():
                tool_input = tool_input.replace(k, v)
                step_name = step_name.replace(k, v)
            plan += f"Plan: {_plan}\n{step_name} = {tool}[{tool_input}]"

        result = self.solver.run(state={
            "plan": plan, 
            "task": state["task"]
        })

        return {"result": result.content}
        
    def _get_current_task(self, state: ReWOO):
        if state["results"] is None:
            return 1
        if len(state["results"]) == len(state["steps"]):
            return None
        else:
            return len(state["results"]) + 1

    def tool_execution(self, state: ReWOO):
        """Worker node that executes the tools of a given plan."""
        _step = self._get_current_task(state)
        _, step_name, tool, tool_input = state["steps"][_step - 1]
        _results = state["results"] or {}

        for k, v in _results.items():
            tool_input = tool_input.replace(k, v)

        try: 
            match tool: 
                case "Tavily": 
                    result = self.search_engine.run(tool_input)
                case "LLM": 
                    result = self.llm_engine.run(tool_input)
        except:
            raise ValueError
        
        _results[step_name] = str(result)
        return {"results": _results}