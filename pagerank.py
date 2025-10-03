import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    linked_pages = corpus[page]    

    # If page has no outgoing links, then transition_model 
    # should return a probability distribution that 
    # chooses randomly among all pages with equal probability. 
    if len(linked_pages) == 0:
        prob = 1 / len(corpus)
        prob_dist = {key: prob for key in corpus}
        return prob_dist


    prob_dist = {key: 0 for key in corpus}

    # With probability `damping_factor`, 
    # choose a link at random linked to by `page`
    link_prob = damping_factor / len(linked_pages)
    for lp in linked_pages:
        prob_dist[lp] += link_prob

    # With probability `1 - damping_factor`, choose a 
    # link at random chosen from all pages in the corpus.
    page_prob = (1 - damping_factor) / len(corpus)
    for key_page in prob_dist:
        prob_dist[key_page] += page_prob
    
    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    pagerank = {key: 0 for key in corpus}
    
    # First sample: randomly chosen page    
    page = random.choice(list(corpus.keys()))
    pagerank[page] += 1

    for _ in range(n - 1):
        prob_dist = transition_model(corpus, page, damping_factor)
        page = random.choices(
            population = list(prob_dist.keys()),
            weights = list(prob_dist.values()),
            k = 1
        )[0]
        pagerank[page] += 1

    # Get probabilities
    pagerank_prob = {key: value / n for key, value in pagerank.items()}
    return pagerank_prob


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    n = len(corpus)
    pagerank = {key: 1 / n for key in corpus}

    convergence = 0.001

    while True:
        max_covergence = 0
        new_pagerank= {}

        # Rank of pages without links
        rank_no_link = 0
        for page, links in corpus.items():
            if len(links) == 0:
                rank_no_link += pagerank[page] / n

        for page in corpus:
            # Add page rank
            new_rank = (1 - damping_factor) / n

            # Add rank of pages without links 
            new_rank += damping_factor * rank_no_link

            # Add rank of pages i
            sum_page_i = 0
            for page_i, page_i_links in corpus.items():
                if page in page_i_links:
                    n_links = len(page_i_links)
                    sum_page_i += pagerank[page_i] / n_links            
            
            new_rank += damping_factor * sum_page_i

            # Compare old rank with new rank
            change = abs(new_rank - pagerank[page])
            max_covergence = max(max_covergence, change)
            new_pagerank[page] = new_rank

        pagerank = new_pagerank

        if max_covergence < convergence:
            break

    # Normalize probabilities to sum = 1
    s = sum(pagerank.values())
    pagerank_normalized = {key: value / s for key, value in pagerank.items()}    
    return pagerank_normalized


if __name__ == "__main__":
    main()
