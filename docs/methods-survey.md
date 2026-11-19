# 頂尖期刊方法盤點

這一頁回答一個問題：**2024–2026 年發表在影響係數 20 以上期刊的 GWAS 論文，實際用了哪些分析方法？**

## 檢索方式

- **資料庫：** Europe PMC REST API，2026-11-19 檢索。
- **條件：** 標題含「genome-wide association」「genome-wide meta-analysis」或「GWAS」；期刊為 Nature、Nature Genetics、Science、Cell、NEJM 或 Lancet；出版年 2024–2026。
- **結果：** 66 篇，依被引用次數排序。其中絕大多數刊登在 Nature Genetics。
- **選文：** 選取被引用次數高、且 PubMed Central 有全文的人類疾病 GWAS 6 篇，讀取全文 XML 的 Methods 段落。
- **工具比對：** 以工具名稱關鍵字搜尋 Methods 段落，再人工閱讀關鍵段落確認用途。下表「方法段落提到的工具」是關鍵字比對結果，代表該工具出現在方法段落中；具體用途以各章引用的原文描述為準。

期刊影響係數（取自各期刊 Wikipedia 條目，2026-11-19 擷取；正式數字請以 JCR 為準）：Nature Genetics 25.5（2025）、Nature 56.1（2025）、Science 45.8（2024）、Cell 45.5（2023）。

## 六篇論文

| 論文 | 規模 | 方法段落提到的工具（關鍵字比對） |
|---|---|---|
| Kim et al., 2024, *Nat Genet* 56:27-36<br>多族群帕金森氏症 | 49,049 病例、18,785 代理病例、2,458,063 對照 | PLINK、MR-MEGA、LD score、SMR、HEIDI、MAGMA、FUMA、Minimac、Eagle、1000 Genomes、GTEx、ANNOVAR |
| Meng et al., 2024, *Nat Genet* 56:222-233<br>多族群憂鬱症 | 新增 88,316 病例、902,757 對照 | PLINK、SAIGE、BOLT-LMM、GCTA、METAL、LDSC、coloc、MAGMA、FUMA、FUSION／TWAS、TwoSampleMR、GTEx |
| Tadros et al., 2025, *Nat Genet* 57:530-538<br>肥厚型心肌病變 | 5,900 病例、68,359 對照，加 36,083 名 UK Biobank 心臟 MRI 參與者 | REGENIE、BOLT-LMM、GCTA、GWAMA、LDSC、S-LDSC、coloc、MAGMA、FUMA、PrediXcan／TWAS、TwoSampleMR、MR-PRESSO、gnomAD、VEP、GTEx |
| Henry et al., 2025, *Nat Genet* 57:815-828<br>心臟衰竭與亞型 | 190 萬人，其中 153,174 人有心臟衰竭 | PLINK、GCTA、METAL、MR-MEGA、LDSC、SuSiE、PolyFun、coloc、MAGMA、PoPS、TWAS、LDpred、CADD、LDAK |
| Lammi et al., 2025, *Nat Genet* 57:1402-1417<br>長新冠 | 最多 6,450 病例、1,093,995 對照，24 個研究 | PLINK、REGENIE、SAIGE、coloc、TwoSampleMR、MR-PRESSO、gnomAD、GTEx、Open Targets |
| Strom et al., 2026, *Nat Genet* 58:275-288<br>焦慮症 | 122,341 病例、729,881 對照 | PLINK、GCTA、METAL、LDSC、FINEMAP、coloc、SMR、HEIDI、MAGMA、FUMA、GSMR、LDAK、GTEx |

規模數字取自各篇摘要。

## 依分析步驟統計

| 分析步驟 | 6 篇中提到的篇數 | 常見工具 | 本課程章節 |
|---|---|---|---|
| 基因型填補 | 1（關鍵字比對；多數論文在補充資料說明各世代的填補方式） | Eagle、Minimac、1000 Genomes 參考面板 | [L08](chapters/L08.md) |
| 關聯分析 | 6 | PLINK、REGENIE、SAIGE、BOLT-LMM | [L09](chapters/L09.md) |
| 統合分析 | 5 | METAL、GWAMA、MR-MEGA | [L11](chapters/L11.md) |
| 遺傳力與遺傳相關 | 5 | LDSC、S-LDSC | [L11](chapters/L11.md) |
| 精細定位 | 2（關鍵字比對） | SuSiE＋PolyFun、FINEMAP | [L12](chapters/L12.md) |
| 共定位與表現量整合 | 6 | coloc、SMR／HEIDI、TWAS | [L12](chapters/L12.md) |
| 基因與基因集分析 | 5 | MAGMA、FUMA、PoPS | [L12](chapters/L12.md) |
| 孟德爾隨機化 | 4 | TwoSampleMR、MR-PRESSO、GSMR | [L13](chapters/L13.md) |
| 多基因風險分數 | 2 | LDpred2、MegaPRS（LDAK） | [L13](chapters/L13.md) |

「篇數」以關鍵字出現在方法段落計算。例如憂鬱症論文摘要提到 fine mapping，但方法段落沒有出現本表比對的精細定位工具名稱，因此沒有計入精細定位。

## 從盤點看到的趨勢

1. **多族群是主流。** 6 篇中有 2 篇標題就標明 multi-ancestry，心臟衰竭論文也以 MR-MEGA 評估跨族群的效應異質性；Pan-UK Biobank（Karczewski et al., 2025）則強調納入多元祖源的樣本。
2. **混合模型與 REGENIE 已是大型生物資料庫的預設。** 長新冠國際合作的分析計畫建議各世代使用 REGENIE。
3. **單一方法不足以指認致病基因。** 論文普遍同時使用共定位、SMR、TWAS、MAGMA、PoPS，並以多種證據交集決定優先基因。
4. **後續分析多半只需要摘要統計。** 這讓沒有個人層級資料的研究生，也能用公開摘要統計練習頂尖期刊的大部分方法。

## 檢索到的其他高被引論文（節錄）

| 論文 | 期刊與年份 | DOI |
|---|---|---|
| Genome-wide association analyses identify 95 risk loci and provide insights into the neurobiology of post-traumatic stress disorder | Nat Genet 2024 | 10.1038/s41588-024-01707-9 |
| Pan-UK Biobank genome-wide association analyses enhance discovery and resolution of ancestry-enriched effects | Nat Genet 2025 | 10.1038/s41588-025-02335-7 |
| Gene discovery and biological insights into anxiety disorders from a large-scale multi-ancestry genome-wide association study | Nat Genet 2024 | 10.1038/s41588-024-01908-2 |
| MESuSiE enables scalable and powerful multi-ancestry fine-mapping of causal variants in genome-wide association studies | Nat Genet 2024 | 10.1038/s41588-023-01604-7 |
| A multi-cohort genome-wide association study in African ancestry individuals reveals risk loci for primary open-angle glaucoma | Cell 2024 | 10.1016/j.cell.2023.12.006 |
| Secure and federated genome-wide association studies for biobank-scale datasets | Nat Genet 2025 | 10.1038/s41588-025-02109-1 |
| Valid inference for machine learning-assisted genome-wide association studies | Nat Genet 2024 | 10.1038/s41588-024-01934-0 |
| Family-based genome-wide association study designs for increased power and robustness | Nat Genet 2025 | 10.1038/s41588-025-02118-0 |
| Multiancestry conditional and joint analysis applied to GWAS summary statistics | Nat Genet 2026 | 10.1038/s41588-026-02799-1 |

後四篇是方法學論文，適合有興趣的學生延伸閱讀，也可作為期末專題選文。

## 參考文獻

- Kim JJ, et al. Multi-ancestry genome-wide association meta-analysis of Parkinson's disease. *Nat Genet*. 2024;56:27-36. doi:10.1038/s41588-023-01584-8
- Meng X, et al. Multi-ancestry genome-wide association study of major depression aids locus discovery, fine mapping, gene prioritization and causal inference. *Nat Genet*. 2024;56:222-233. doi:10.1038/s41588-023-01596-4
- Tadros R, et al. Large-scale genome-wide association analyses identify novel genetic loci and mechanisms in hypertrophic cardiomyopathy. *Nat Genet*. 2025;57:530-538. doi:10.1038/s41588-025-02087-4
- Henry A, et al. Genome-wide association study meta-analysis provides insights into the etiology of heart failure and its subtypes. *Nat Genet*. 2025;57:815-828. doi:10.1038/s41588-024-02064-3
- Lammi V, et al. Genome-wide association study of long COVID. *Nat Genet*. 2025;57:1402-1417. doi:10.1038/s41588-025-02100-w
- Strom NI, et al. Genome-wide association study of major anxiety disorders in 122,341 European-ancestry cases identifies 58 loci and highlights GABAergic signaling. *Nat Genet*. 2026;58:275-288. doi:10.1038/s41588-025-02485-8
- Karczewski KJ, et al. Pan-UK Biobank genome-wide association analyses enhance discovery and resolution of ancestry-enriched effects. *Nat Genet*. 2025;57:2408-2417. doi:10.1038/s41588-025-02335-7
