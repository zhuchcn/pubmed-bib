import click
import requests
import json

# Get a reference from PubMed database
def getReference(id):
    url_format = 'https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pubmed/'
    # Parameters for query
    queryParams = {
        'format': 'csl',
        'id': id
    }
    # get a reference
    response = requests.get(url_format, params = queryParams).json()
    return response

# Format the reference to BibTex format
def formatReference(reference):
    title = reference['title'] if 'title' in reference.keys() else ''
    authors = reference['author'] if 'author' in reference.keys() else ''
    authorList = []
    for author in authors:
        if ('family' in author.keys()) and ('given' in author.keys()):
            authorList.append(author['family'] + ', ' + author['given'])
        elif ('family' in author.keys()) and ('given' not in author.keys()):
            authorList.append(author['family'])
        elif ('family' not in author.keys()) and ('given' in author.keys()):
            authorList.append(author['given'])
        else:
            continue

    journal = reference['container-title'] if 'container-title' in reference.keys() else ''
    volume = reference['volume'] if 'volume' in reference.keys() else ''
    page = reference['page'] if 'page' in reference.keys() else ''
    if 'issued' in reference.keys():
        year = reference['issued']['date-parts'][0][0]
    elif 'epub-date' in reference.keys():
        year = reference['epub-date']['date-parts'][0][0]    

    output = f'''@article{{{ authorList[0].split(' ')[0].lower() + str(year) + title.split(' ')[0].lower() },
    title={{{title}}},
    author={{{' and '.join(authorList)}}},
    journal={{{journal}}},
    volume={{{volume}}},
    pages={{{page}}},
    year={{{year}}}
}}'''
    return output

def showReference(id):
    '''
    Get the BibTex styled reference from a given PMID from the PubMed database using PubMed's API
    '''
    # Get the reference from PubMed
    reference = getReference(id)        
    # I the reference is not found
    if 'status' in reference.keys() and reference['status'] == 'error' :
        output = 'Reference not found'
    else:
        output = f'The BibTex for the reference with PMID={id} is:\n' + formatReference(reference)

    click.echo(output)
    return 

def convertReferences(input_file, output_file):
    # Read all PMIDs in
    id = []
    successNumber, failNumber = 0, 0
    with open(input_file) as ih:
        with open(output_file, 'w') as oh:
            for line in ih:
                ref = getReference(line.rstrip())
                if 'status' in ref.keys() and ref['status'] == 'error' :
                    print(f'PMID {line.rstrip()} NOT FOUND')
                    failNumber += 1
                else: 
                    ref = formatReference(ref)
                    successNumber += 1
                    oh.write(ref+'\n')
    print(f'{successNumber} reference{"s" if successNumber > 1 else ""} retrieved.\n{failNumber} reference{"s" if failNumber > 1 else ""} not found.')
    return

@click.command()
@click.option('--id', default=None,  help="The PubMed PMID.")
@click.option('--input-file', default=None, help='A text file with list of PMID')
@click.option('--output-file', default=None, help='The output file to store BibTex styled references')
def pubMed2BibTex(id, input_file, output_file):
    '''
    Retrieve article reference from PubMed in BibTex format.
    '''
    if id:
        showReference(id)
    elif input_file and output_file:
        convertReferences(input_file, output_file)
    else:
        return

if __name__ == '__main__':
    pubMed2BibTex()