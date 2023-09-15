# BELEBELE_LV_EVAL
Skripts sagatavo visus promptus no Meta [belebele](https://github.com/facebookresearch/belebele) datu kopas, bet tālāk prompti tiek vadīti manuāli, jo:

- Nav OpenAI API key automatizēšanai.
- Uz sava datora nevaru palaist inference lieliem modeļiem.
- OpenAI API tāpat būtu 3 prompti minūtē ierobežojums.

Attiecīgi process ir lēns un laikietilpīgs. Rezultāti tiks ik pa laikam papildināti.

## Rezultāti

| Modelis              | Rezultāts, % | Jautājumi | Pareizi |
|----------------------|--------------|-----------|---------|
| ChatGPT-4            | 91.49        | 47/900    | 43/47   |
| ChatGPT-3.5          | 60           | 20/900    | 12/20   |
| Llama-2-70B-chat-hf* | 30           | 20/900    | 6/20    |
| Minēšana             | 25           | 900/900   | 900/900 |

*[Llama-2-70B-chat-hf](https://huggingface.co/spaces/akdeniz27/LLaMa-2-70b-chat-hf-with-EasyLLM)

Pēdējās izmaiņas: 2023. gada 15. septembris 15:10.

## Prompts

```
"""{flores_passage}
        
{question}

Atbilžu varianti:

1: {mc_answer1}
2: {mc_answer2}
3: {mc_answer3}
4: {mc_answer4}

Sniedz atbildi pēc formāta "Pareizā atbilde: <tava atbilde>".
```

Potenciāli uzlabojumi:

- Specifiskākas prasības atbildei: šobrīd reizēm atbild ar cipari, reizēm ar pašu atbildi.
- Chain-of-Thought: Prasīt paskaidrot pareizo atbildi.
- Reflection: Pārjautāt modelim, vai tā sniegtā atbilde ir pareiza, kā arī, vai tā atbilst atbildes formatēšanas nosacījumiem?