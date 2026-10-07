from prometheus_client import Counter, Histogram


class AgentMetrics:
    def __init__(self):
        self.agent_runs = Counter(
            "agent_runs_total",
            "Total number of new agent runs.",
        )

        self.agent_status = Counter(
            "agent_status_total",
            "Total number of agent status transitions.",
            ["status"],
        )

        self.llm_calls = Counter(
            "agent_llm_calls_total",
            "Total number of LLM calls.",
        )

        self.tool_calls = Counter(
            "agent_tool_calls_total",
            "Total number of tool executions.",
            ["tool_name"],
        )

        self.llm_latency = Histogram(
            "agent_llm_latency_seconds",
            "LLM call latency in seconds.",
        )

        self.tool_latency = Histogram(
            "agent_tool_latency_seconds",
            "Tool execution latency in seconds.",
            ["tool_name"],
        )

    def increment_agent_runs(self):
        self.agent_runs.inc()

    def increment_agent_status(self, status: str):
        self.agent_status.labels(status=status).inc()

    def increment_llm_calls(self):
        self.llm_calls.inc()

    def increment_tool_calls(self, tool_name: str):
        self.tool_calls.labels(tool_name=tool_name).inc()

    def observe_llm_latency(self, seconds: float):
        self.llm_latency.observe(seconds)

    def observe_tool_latency(
        self,
        tool_name: str,
        seconds: float,
    ):
        self.tool_latency.labels(tool_name=tool_name).observe(seconds)
