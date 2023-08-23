import asyncio

# List of available trade pairs
trade_pairs = ["ETH - USDT", "ETH - WBTC", "USDT - ETH", "WBTC - ETH"]

# Simulating an asynchronous swap function
async def swap(client, wofi_client, pair, amount):
    # Your swap logic here
    pass

async def main():
    # Display available trade pairs to the user
    print("Please choose a pair to SWAP:")
    for index, pair in enumerate(trade_pairs, start=1):
        print(f"{index}. {pair}")

    # Get user's choice
    user_choice = int(input("Enter the number of the pair you want to choose: "))

    # Validate user's choice
    if 1 <= user_choice <= len(trade_pairs):
        selected_pair = trade_pairs[user_choice - 1]
        print("You have chosen:", selected_pair)

        await asyncio.sleep(1)  # Simulating some async task

        await swap(client, WooFi(client=Client), selected_pair, amount)

    else:
        print("Invalid choice. Please choose a valid number.")

# Run the async function in the asyncio event loop
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
