# bibtex automation
Welcome to the Bibliography Automation Tool GitHub repository!

Are you tired of manually formatting citations for your research papers and projects? Look no further! This project offers a powerful solution for automating bibliography management, saving you time and ensuring accuracy in your references.

## Description
Introducing the Bibliography Automation Tool GitHub repository! Simplify your research workflow with a powerful citation management solution. Say goodbye to the tedious process of manually formatting citations. Whether you're searching for citations through URLs, using keywords to find relevant titles, or both, this tool streamlines the process and compiles everything into standardized BibTeX format. Experience a more organized approach to bibliography management as all your citations are stored in a single, easily accessible file. Embrace efficiency, accuracy, and open-source flexibility in your academic referencing. Explore the future of citation management with the Bibliography Automation Tool now!

## setup
For installing all needed packages , run the following command

```
pip install -r requirements.txt
```
## Getting started
To use this tool , run the following command 
```
py references_01.py
```
Afterward, you'll be presented with four user-friendly options, each designed for different publication sites and methods of searching for books.

it will looks as following :
```
Options :
1 - dblp text entry
2 - dblp url entry
3 - arxiv text entry
4 - springer url entry
Enter your choice :
```
Select your preferred publication site and search method .

### Exploring Options
1. dblp Text Entry: Discover Books through Keyword Search

Explore a vast collection of books by entering relevant keywords. The system intelligently retrieves titles that precisely match the entered keywords or offers an extended search to include related terms.

2. dblp URL Entry: Retrieve Specific Book via URL

Streamline your search by entering a direct URL from dblp for the exact book you're looking for. Effortlessly access bibliographic details for your chosen publication.

3. arXiv Text Entry: Uncover Books via Keyword Search

Seamlessly find books by initiating searches with specific keywords. The system returns titles that align with the exact keywords provided, or it can broaden the search to encompass related terms.

4. Springer URL Entry: Access Precise Book Information via URL

Enhance your efficiency by inputting a Springer URL for the specific book you're interested in. Gain quick access to comprehensive bibliographic information for your selected publication.

## Excpected Outcome 

Once you've used any of the provided options ,the retrieved citations will bes aved in a file called : 
```
myfile.bib
```
This organized bibliography file serves as a valuable resource, perfectly suited for integration into your academic writing, particularly when working with LaTeX or other platforms. With this collection of citations, you'll experience enhanced efficiency and accuracy in referencing, allowing you to focus on the substance of your research and writing.