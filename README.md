## Rezultāti

Vieta | Modelis              | Rezultāts, % | Pareizi | Izstrādātājs | Open source | Datums     |
------|----------------------|--------------|---------|--------------|-------------|------------|
1     | gemini-2.5-pro       | 95.7         | 861     | Google 🇺🇸    | ❌          | 18/08/2025  |
1     | gpt-5                | 95.7         | 861     | OpenAI 🇺🇸    | ❌          | 20/08/2025  |                
3     | gemini-2.5-flash     | 95.4         | 859     | Google 🇺🇸    | ❌          | 18/08/2025  |
3     | gpt-5-mini           | 95.4         | 859     | OpenAI 🇺🇸    | ❌          | 19/08/2025  |
5     | gpt-5-nano           | 89.1         | 802     | OpenAI 🇺🇸    | ❌          | 19/08/2025  |

### 📝 Piezīmes

- Kopējais jautājumu skaits: 900. 
- Visiem modeļiem izvērtēšana veikta tikai 1 reizi.
- Pēdējās izmaiņas: 2025. gada 19. augusts.

Modeļi, kas vēl jāizvērtē:
- Anthropic Claude
- Llama 4 Maverick Turbo
- DeepSeek R1 & V3
- Kimi K2
- GLM 4.5
- Qwen 3
- Grok 4
- Mistral

## Izmantotā vaicājuma šablons

```
Atbildi uz jautājumu par teksta fragmentu, izvēloties pareizo atbilžu variantu:

{flores_passage}
        
{question}

1) {mc_answer1}
2) {mc_answer2}
3) {mc_answer3}
4) {mc_answer4}
```

Atbilde, kas tiek saņemta no valodas modeļa ir A, B, C vai D. Bez paskaidrojuma. Ir iestrādāta opcija atgriezt un saglabāt modeļa atbildes paskaidrojumus. Tās ieslēgšana visticamāk uzlabo modeļa rezultātu, bet izmaksu dēļ šo rezultātu iegūšanā tas netika darīts.