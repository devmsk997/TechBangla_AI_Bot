emporarily unavailable.
Retrying in 20 seconds...
Trying model: gemini-3.6-flash | Attempt 3/5
Gemini Error: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experienc
ing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAI
LABLE'}}
⚠️ Gemini temporarily unavailable.
Retrying in 40 seconds...
Trying model: gemini-3.6-flash | Attempt 4/5
Gemini Error: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experienc
ing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAI
LABLE'}}
⚠️ Gemini temporarily unavailable.
Retrying in 80 seconds...
Trying model: gemini-3.6-flash | Attempt 5/5
Gemini Error: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experienc
ing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAI
LABLE'}}
⚠️ Gemini temporarily unavailable.
Retrying in 90 seconds...
Traceback (most recent call last):
  File "H:\MY AUTO BOTS\TechBangla_AI_Bot\main.py", line 120, in <module>
    main()
    ~~~~^^
  File "H:\MY AUTO BOTS\TechBangla_AI_Bot\main.py", line 63, in main
    raw_article = generate_article(topic, category, keywords)
  File "H:\MY AUTO BOTS\TechBangla_AI_Bot\gemini_writer.py", line 238, in generate_article
    raise Exception(
    ...<2 lines>...
    )
Exception: Gemini generation failed after all retries: 503 UNAVAILABLE. {'error': {'code': 503, 'mes
sage': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Pl
ease try again later.', 'status': 'UNAVAILABLE'}}

User@DESKTOP-MQDT980 MINGW64 /h/MY AUTO BOTS/TechBangla_AI_Bot (main)
