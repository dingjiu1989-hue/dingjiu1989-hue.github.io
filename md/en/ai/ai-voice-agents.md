---
title: "Building AI Voice Agents: Complete Technical Guide (2026)"
description: "How to build real-time AI voice agents: STT (Whisper) + LLM (GPT-4o/Claude) + TTS (ElevenLabs). Covers WebRTC streaming, latency optimization, voice activity detection, and interruption handling."
date: 2026-05-08
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/ai-voice-agents.html
---

# Building AI Voice Agents: Complete Technical Guide (2026)

Building a real-time AI voice agent — one that can listen, think, and speak with sub-second latency — was a major engineering challenge two years ago. In 2026, with the GPT-4o real-time API, Claude's voice capabilities, and mature TTS/STT models, it is a weekend project for a competent developer. This guide covers the complete technical stack for building voice agents that feel natural.

## The Voice Agent Pipeline

Stage| Technology| Latency Budget| What Happens  
---|---|---|---  
1\. Audio Input| WebRTC (browser mic)| ~20ms| Raw audio captured from user's microphone  
2\. Speech-to-Text (STT)| OpenAI Whisper, Deepgram, AssemblyAI| 100-300ms| Audio transcribed to text  
3\. LLM Reasoning| GPT-4o, Claude Sonnet, Gemini| 300-1,000ms| AI understands intent and generates response  
4\. Text-to-Speech (TTS)| ElevenLabs, OpenAI TTS, Play.ht| 100-500ms| Text converted to natural speech  
5\. Audio Output| WebRTC (browser speaker)| ~20ms| Audio played to user  
Total (ideal)| —| 500-1,500ms| Target: under 1 second for natural conversation  

## Voice Agent Architecture

    # Simplified voice agent using OpenAI Realtime API
    # The Realtime API combines STT + LLM + TTS into one WebSocket connection
    # Latency: ~500-800ms end-to-end (much faster than chained APIs)

    import asyncio
    import websockets
    import json

    async def voice_agent():
        async with websockets.connect(
            "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime",
            extra_headers={"Authorization": f"Bearer {API_KEY}"}
        ) as ws:
            # Configure the session
            await ws.send(json.dumps({
                "type": "session.update",
                "session": {
                    "modalities": ["text", "audio"],
                    "instructions": "You are a helpful coding mentor. Be concise.",
                    "voice": "alloy",
                    "input_audio_format": "pcm16",
                    "output_audio_format": "pcm16",
                    "turn_detection": {"type": "server_vad"}  # Voice activity detection
                }
            }))

            # Stream audio from browser mic -> ws -> receive audio back
            async for message in ws:
                event = json.loads(message)
                if event["type"] == "response.audio.delta":
                    # Send this audio chunk to browser speaker
                    play_audio(event["delta"])

## STT, LLM, and TTS: Breaking Down the Stack

Component| Best Options| Key Considerations  
---|---|---  
STT (Speech-to-Text)| Deepgram (lowest latency, 100ms), Whisper v3 (best accuracy), AssemblyAI (best features)| Deepgram for real-time; Whisper for batch/offline; AssemblyAI for diarization + sentiment  
LLM| GPT-4o Realtime (all-in-one, best latency), Claude (best reasoning), Gemini (cheapest)| Realtime API eliminates STT/TTS chaining latency; separate STT+LLM+TTS gives more control  
TTS (Text-to-Speech)| ElevenLabs (most natural voices), OpenAI TTS (good + integrated), Play.ht (cloning + emotions)| ElevenLabs for quality; OpenAI for simplicity; Play.ht for custom voice cloning  

## Interruption Handling (Barge-In)

**Critical feature:** Users need to be able to interrupt the AI mid-response (like a human conversation). Implementation: monitor microphone audio level during AI playback. If sustained audio above threshold, immediately stop TTS playback, flush the LLM's partial response, and start listening for the new input. Without interruption handling, the voice agent feels robotic and frustrating.

**Bottom line:** The OpenAI Realtime API is the fastest path to a working voice agent — it bundles STT + LLM + TTS into one low-latency WebSocket. For production, consider Deepgram (STT) + your preferred LLM + ElevenLabs (TTS) for more control over each component. Target under 1 second end-to-end latency for a natural conversation feel. See also: [AI Agents Guide](</en/ai/ai-agents-guide.html>) and [Function Calling Guide](</en/ai/function-calling-guide.html>).
