
LEADERBOARD_ICON_MAP = {
    "Text Leaderboard": "📚",
    "Law": "⚖️",
    "Multilingual": "🌎",
    "German": "🇩🇪",
    "Code": "💻",
    "Tech": "🛠️",
    "Legal": "📜",
    "English": "🇬🇧",
    "Healthcare": "🏥",
    "Finance": "💰",
    "French": "🇫🇷",
    "Japanese": "🇯🇵",

}

LEADERBOARD_DESCRIPTION_MAP = {
    "Text Leaderboard": """Covers overall performance across nearly all text-based datasets in the benchmark. 
This group serves as a broad indicator of a model’s text retrieval capability, aggregating results from diverse domains, topics, and query styles into one unified score. 
It is ideal for assessing general-purpose models intended for a wide range of retrieval applications, such as search, recommendation, and RAG. 
The datasets span multiple fields—from news and encyclopedias to specialized archives—offering a balanced mix of short and long queries, varied complexity, and real-world relevance. 
A high score here reflects versatility and robustness in text retrieval across different contexts.""",

    "Law": """Focuses on legal information retrieval, including case law, statutes, contracts, and legal commentary. 
The datasets may cover multiple jurisdictions and languages, ensuring that models are tested on domain-specific terminology and complex hierarchical structures in legal writing. 
This group is essential for applications such as legal research tools, contract analysis systems, and compliance-checking solutions. 
It evaluates whether a model can accurately match legal queries to relevant documents, maintain contextual precision, and handle nuanced phrasing found in legal discourse. 
Performance here often requires specialized knowledge and the ability to generalize across sub-domains within law.""",

    "Multilingual": """Evaluates retrieval capabilities in multi-language and cross-lingual settings. 
Datasets include queries and documents in various languages, as well as scenarios where the query language differs from the document language. 
The group measures a model’s ability to generalize semantic understanding across linguistic boundaries without losing retrieval accuracy. 
It is crucial for global applications where users interact with content in different languages, such as multilingual search engines, cross-border information services, and international customer support. 
High performance here reflects strong language-agnostic embedding quality and effective handling of tokenization and encoding challenges.""",

    "German": """Specializes in retrieval tasks involving the German language, both in monolingual and cross-lingual contexts. 
Datasets may cover domains such as law, news, technical documentation, and academic literature in German. 
This group evaluates whether a model can capture the linguistic nuances, compound words, and syntactic structures unique to German, while also enabling accurate retrieval in cross-language queries. 
It is highly relevant for localized applications in German-speaking regions and for multilingual systems that must maintain parity in performance across different languages.""",

    "Code": """Targets source code retrieval and programming-related search tasks. 
Datasets pair code snippets with relevant documentation, bug reports, or explanatory text. 
This group tests whether a model can understand syntax, semantics, and the functional meaning of code in various programming languages. 
It is particularly valuable for code search engines, automated documentation assistants, and developer productivity tools. 
Strong performance here demonstrates a model’s ability to link natural language queries with precise technical code matches, a capability crucial in software engineering workflows.""",

    "Tech": """Covers retrieval tasks in the technology domain, including software, hardware, engineering, and scientific innovation. 
Datasets may include technical manuals, product specifications, API references, and research papers. 
This group evaluates a model’s ability to handle domain-specific jargon, structured information, and precise definitions common in technical documents. 
It is suited for applications like technical support search, product documentation systems, and R&D information retrieval. 
A high score here indicates the model’s strength in specialized technical contexts where precision is critical.""",

    "Legal": """Covers broader legal-domain retrieval beyond the case-focused 'Law' group, potentially including regulatory guidelines, compliance checklists, policy documents, and government reports. 
This group emphasizes models’ capacity to connect queries to relevant legal resources, even when documents are less formal or more practical in nature than case law. 
It is essential for corporate compliance, governance documentation search, and legal advisory systems. 
Performance in this group reflects the ability to work across varying legal writing styles and document structures.""",

    "English": """Focuses on retrieval tasks in the English language, covering both general-purpose and domain-specific content. 
Datasets may include web articles, academic papers, legal documents, and conversational transcripts. 
The group measures the ability to handle English-specific syntax, idioms, and stylistic variety while maintaining high relevance in results. 
It is key for English-dominant markets and also serves as a baseline for multilingual models. 
High scores here typically correlate with strong overall retrieval performance, given the abundance of English-language datasets in the benchmark.""",

    "Healthcare": """Evaluates retrieval performance in the medical and healthcare domain. 
Datasets may include clinical guidelines, research literature, case studies, and patient education materials. 
The group tests the ability to handle specialized medical terminology, abbreviations, and structured knowledge formats. 
It is essential for applications such as clinical decision support systems, medical literature search, and health information portals. 
Accuracy in this group requires domain awareness and sensitivity to critical details, as retrieval errors can have significant consequences in healthcare contexts.""",

    "Finance": """Covers retrieval tasks in the financial domain, including corporate filings, market research, investment analysis, and economic reports. 
This group tests whether a model can accurately interpret and retrieve financial content, including numerical data, specialized terms, and regulatory language. 
It is suited for applications like investment research platforms, corporate intelligence tools, and financial news aggregation. 
High scores in this group reflect the ability to handle domain-specific vocabulary and data-driven queries with precision.""",

    "French": """Specializes in retrieval tasks involving the French language, covering monolingual and cross-lingual scenarios. 
Datasets may span domains such as news, legal documents, academic publications, and technical manuals in French. 
The group evaluates whether a model can process French morphology, idiomatic expressions, and syntactic structure while maintaining semantic accuracy. 
It is important for localized systems serving French-speaking regions and for multilingual applications requiring consistent quality across languages.""",

    "Japanese": """Focuses on retrieval in the Japanese language, including both monolingual and cross-lingual contexts. 
Datasets may involve business documents, technical resources, news, and conversational text in Japanese. 
This group tests a model’s ability to handle Japanese writing systems (kanji, hiragana, katakana), segmentation challenges, and culturally specific terminology. 
It is critical for applications in Japanese markets and for multilingual systems supporting East Asian languages. 
High performance here indicates adaptability to complex linguistic features and script diversity."""
}
