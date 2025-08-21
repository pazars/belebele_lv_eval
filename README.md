## Rezultāti

Vieta | Modelis                       | Rezultāts, % | Pareizi | Izstrādātājs   | Open source | Datums     |
------|-------------------------------|--------------|---------|----------------|-------------|------------|
1     | gemini-2.5-pro                | 95.7         | 861     | Google 🇺🇸            | ❌     | 18/08/2025  |
1     | gpt-5                         | 95.7         | 861     | OpenAI 🇺🇸            | ❌     | 20/08/2025  |                
3     | gemini-2.5-flash              | 95.4         | 859     | Google 🇺🇸            | ❌     | 18/08/2025  |
3     | gpt-5-mini                    | 95.4         | 859     | OpenAI 🇺🇸            | ❌     | 19/08/2025  |
5     | DeepSeek-R1-0528-Turbo        | 94.6         | 851     | DeepSeek 🇨🇳          | ✅     | 21/08/2025  |
6     | GLM-4.5                       | 93.4         | 841     | Z AI 🇨🇳              | ✅     | 21/08/2025  |
7     | Qwen3-235B-A22B-Instruct-2507 | 93.1         | 838     | Alibaba Cloud 🇨🇳     | ✅     | 20/08/2025  |
8     | gpt-oss-120b                  | 91.6         | 824     | OpenAI 🇺🇸            | ✅     | 21/08/2025  |
9     | DeepSeek-V3-0324              | 91.0         | 819     | DeepSeek 🇨🇳          | ✅     | 21/08/2025  |
10    | kimi-latest                   | 90.0         | 810     | Moonshot AI 🇨🇳       | ❓     | 20/08/2025  |
11    | gpt-5-nano                    | 89.1         | 802     | OpenAI 🇺🇸            | ❌     | 19/08/2025  |

### 📝 Piezīmes

- Kopējais jautājumu skaits: 900. 
- Visiem modeļiem izvērtēšana veikta tikai 1 reizi.
- Pēdējās izmaiņas: 2025. gada 19. augusts.

Modeļi, kurus neizdevās izvērtēt:

Modelis           | Izstrādātājs   | Komentārs                         | Datums     |
------------------|----------------|-----------------------------------|------------|
command-a-03-2025 | Cohere 🇨🇦       | Atbilžu validācijas problēmas    | 20/08/2025 |
Kimi-K2-Instruct  | Moonshot AI 🇨🇳  | Atbilžu validācijas problēmas    | 21/08/2025 |

Modeļi, kas vēl jāizvērtē:
- Anthropic Claude
- Llama 4 Maverick Turbo
- Kimi K2
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