# Convert PubMed ID (PMID) to BibTex Reference

This is a very simple tool that searches the given PMID(s) using PubMed's REST api, get the reference information, and convert to a BibTex format. 

## Installation

```
$ git clone https://github.com/zhuchcn/pubmed-bib.git
$ cd pubmed-bib
$ pip install -e .
```

## Search a single PMID
A single PMID can be searched using following command.

```
$ pubmed-bib --id 30440093
```

A reference record in BibTex format will be printed in terminal.

```
@article{park2018evaluation,
    title={Evaluation of gastric microbiome and metagenomic function in patients with intestinal metaplasia using 16S rRNA gene sequencing},
    author={Park, Chan Hyuk and Lee, A-Reum and Lee, Yu-Ra and Eun, Chang Soo and Lee, Sang Kil and Han, Dong Soo},
    journal={Helicobacter},
    volume={},
    pages={e12547},
    year={2018}
}
```

Or append a reference ot an existing BibTex file

```
$ pubmed-bib --id 30440093 --output-file reference.bib
```

## Batch search
A batch search can be done by providing a `.txt` file with a PMID in each line, and all references are ready for you.

```
pubmed-bib --input-file pmid.txt --output-file references.bib
```