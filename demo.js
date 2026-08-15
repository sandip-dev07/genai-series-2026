const data = [
  HumanMessage(
    (content = "hi"),
    (additional_kwargs = {}),
    (response_metadata = {}),
    (id = "44bd1def-1e54-47ef-906c-436aa1c63a39"),
  ),
  AIMessage(
    (content = "Hello! How can I help you manage your tasks today?"),
    (additional_kwargs = {
      reasoning_content:
        'User says "hi". We need to respond. No database query needed.',
    }),
    (id = "lc_run--01a00648-565d-7290-bfd8-25dca101ac76-0"),
    (tool_calls = []),
    (invalid_tool_calls = []),
    (usage_metadata = {
      input_tokens: 555,
      output_tokens: 37,
      total_tokens: 592,
      output_token_details: { reasoning: 16 },
    }),
  ),
];


console.log(data);

