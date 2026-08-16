{
  messages: [
    HumanMessage(
      (content = "hi"),
      (additional_kwargs = {}),
      (response_metadata = {}),
      (id = "71d80914-19ac-4eed-ac7a-752b2916a56e"),
    ),
    AIMessage(
      (content =
        "Hello! 👋  \nHow can I help you manage your tasks today?  \n- Add a new task  \n- Update a task’s status  \n- Delete a task  \n- Show me a list of tasks  \n\nJust let me know what you’d like to do!"),
      (additional_kwargs = {
        reasoning_content:
          'User says "hi". We need to respond as a task management assistant. Probably greet and ask how can help.',
      }),
      (response_metadata = {
        token_usage: {
          completion_tokens: 86,
          prompt_tokens: 579,
          total_tokens: 665,
          completion_time: 0.089826705,
          completion_tokens_details: { reasoning_tokens: 24 },
          prompt_time: 0.031205502,
          prompt_tokens_details: None,
          queue_time: 0.367850565,
          total_time: 0.121032207,
        },
        model_name: "openai/gpt-oss-20b",
        system_fingerprint: "fp_d23c14756c",
        service_tier: "on_demand",
        finish_reason: "stop",
        logprobs: None,
        model_provider: "groq",
      }),
      (id = "lc_run--01a00967-4ac3-7080-9edf-699485f8c7f0-0"),
      (tool_calls = []),
      (invalid_tool_calls = []),
      (usage_metadata = {
        input_tokens: 579,
        output_tokens: 86,
        total_tokens: 665,
        output_token_details: { reasoning: 24 },
      }),
    ),
  ];
}
