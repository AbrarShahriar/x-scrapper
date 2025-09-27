import asyncio

from twikit.guest import GuestClient

client = GuestClient()


async def main():
    # Activate the client by generating a guest token.
    await client.activate()

    user = await client.get_user_by_screen_name("Linus__Torvalds")
    user_tweets = await user.get_tweets()

    for tweet in user_tweets:
        print(tweet.text)

asyncio.run(main())