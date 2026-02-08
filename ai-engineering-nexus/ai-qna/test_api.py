import pytest
from httpx import ASGITransport, AsyncClient
from main import app

@pytest.mark.asyncio
async def test_async_stream():
    # Use AsyncClient for async endpoints
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        async with ac.stream("POST", "/ask?question=Write a poem") as response:
            assert response.status_code == 200
            
            chunks = []
            # 3. Iterate over the incoming text chunks
            async for text in response.aiter_text():
                chunks.append(text)
                # print(f"Received chunk: {text}") # Optional debugging
            
            # 4. Verify the final result
            full_text = "".join(chunks)
            assert len(chunks) > 0
            assert "data:" in full_text  # If using SSE format

@pytest.mark.asyncio
async def test_chat1():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response1 = await ac.post(
            '/chat?message=Hi'
        )
        assert response1.status_code == 200
        content1 = response1.json()  # or response.text
        cookies = response1.cookies
        assert "hello" in content1.lower()
        
        response2 = await ac.post(
            '/chat?message=My name is Shashwat',
            cookies = cookies
        )
        assert response2.status_code == 200

        response3 = await ac.post(
            '/chat?message=What is my name?',
            cookies = cookies
        )
        assert response3.status_code == 200
        content3 = response3.json()  # or response.text
        assert "shashwat" in content3.lower()