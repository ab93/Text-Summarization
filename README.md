# Spanish Text Summarization using Keyword Extraction
<p align="justify">
This project aims to build a system that can summarize Spanish news articles into concise headlines, using keyword extraction techniques.

This project is part of the course requirements of CSCI 544 Spring 2016 course at the University of Southern California taught by Prof. Ron Artstein. The course can be found at http://ron.artstein.org/csci544-2016/index.html.
</p>

<h2> Introduction </h2>
<p align="justify">
The problem of automatic text summarization is one that has garnered significant interest in recent years. Humans want to read a short gist of a news article before deciding whether or not they want to spend time reading the main article. Hence, there is a need to build computers that can read a piece of text and give a short summary. Automatic document summarization can be done in two ways. We have chosen extractive summarization, which identifies important words/phrases from the source document and creates the summary. Headline generation is a special case of text summarization, which builds a concise headline for a document.

In this project, we propose an approach to summarize and possibly generate headlines for Spanish documents using extractive
summarization techniques. We have experimented with default TextRank algorithm and modified it with our own approach. Our system will be evaluated using ROUGE against the existing TextRank method. 
</p>

<h2> Data </h2>
<p align="justify">
The corpus is a transcript of speeches by two Colombian presidents which has been compiled by an unknown developer from various Internet sources. There are a total of 641 documents. Each document contains some metadata like headline, date, etc.
</p>

<h2> Procedure </h2>
<p align="justify">
The main tasks that our proposed project entails are text
summarization and headline generation. We have achieved
text summarization with our modification on the Text Rank algorithm[1] that performs keyword extraction.
The modification is done based on the intuition that the sentences occuring in the beginning and the end of the text encode more important information about the text or article. We have used an arcsine probability density function that reflects this intuition. This distribution enables us to introduce weights on the textRank graph. Once the top 'n' keywords are extracted, the sentences are scored based on the probability density function with respect to the postion of the sentence and number of keywords present in the sentence. The top 'm' sentences are considered important and are used for the text summarization task.

<br/>
For running the program, do
<br/>
<code>
python get_summary.py file_range_beginning file_range_ending
</code>
<br/>
The summarized text can be obtained by tweaking get_summary.py to write the summary to file. By default, the get_summary.py will give the ROUGE-N score of the original TextRank system and TextRank v2.0.
<br/>

We aim to further experiment with different parameters of the algorithm. They are the window size and stemming/lemmatization prior to the method. Also, as the final part of the project we aim to generate headlines from the extracted keywords using possibly Recurrant Neural Networks (RNN).
</p>

<h2> Evaluation </h2>
<p align="justify">
Since our data doesn't contain human annoted summaries, we have implemented the standard TextRank algorithm for reference. We compare our output with the reference output using ROUGE software. For the headline generation task, we have 322 instances of text with headlines to compare with.
</p>

<h2> References </h2>
[1] R. Mihalcea and P. Tarau. Textrank: Bringing order into texts. Association for Computational Linguistics, 2004
