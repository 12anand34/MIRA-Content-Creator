from mira_sdk import MiraClient, Flow, CompoundFlow
from mira_sdk.exceptions import FlowError
    
    # Initialize MIRA client
client = MiraClient(config={"API_KEY": "sb-85f5913affe3b2faafef48b20480d155"})
print("✓ MIRA client initialized")

flow = CompoundFlow(source="flow.yaml")           # Load flow configuration
print("flow done")
test_input = {                                              # Prepare test inputs
    "prime_input_1": "test data",
    "prime_input_2": "test parameters",
    "prime_input_3": "test parameters"
}
print("input taken")
try:
    response = client.flow.test(flow, test_input)           # Test entire pipeline
    print("Test response:", response)
except FlowError as e:
    print("Test failed:", str(e)) 