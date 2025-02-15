class ProteinToolbox:
    def __init__(self) -> None:
        self.rna_codon_table = {
            "UUU": "F",
            "UUC": "F",
            "UUA": "L",
            "UUG": "L",
            "UCU": "S",
            "UCC": "S",
            "UCA": "S",
            "UCG": "S",
            "UAU": "Y",
            "UAC": "Y",
            "UAA": "Stop",
            "UAG": "Stop",
            "UGU": "C",
            "UGC": "C",
            "UGA": "Stop",
            "UGG": "W",
            "CUU": "L",
            "CUC": "L",
            "CUA": "L",
            "CUG": "L",
            "CCU": "P",
            "CCC": "P",
            "CCA": "P",
            "CCG": "P",
            "CAU": "H",
            "CAC": "H",
            "CAA": "Q",
            "CAG": "Q",
            "CGU": "R",
            "CGC": "R",
            "CGA": "R",
            "CGG": "R",
            "AUU": "I",
            "AUC": "I",
            "AUA": "I",
            "AUG": "M",
            "ACU": "T",
            "ACC": "T",
            "ACA": "T",
            "ACG": "T",
            "AAU": "N",
            "AAC": "N",
            "AAA": "K",
            "AAG": "K",
            "AGU": "S",
            "AGC": "S",
            "AGA": "R",
            "AGG": "R",
            "GUU": "V",
            "GUC": "V",
            "GUA": "V",
            "GUG": "V",
            "GCU": "A",
            "GCC": "A",
            "GCA": "A",
            "GCG": "A",
            "GAU": "D",
            "GAC": "D",
            "GAA": "E",
            "GAG": "E",
            "GGU": "G",
            "GGC": "G",
            "GGA": "G",
            "GGG": "G",
        }

        self.reverse_codon_table = {
            "F": ["UUU", "UUC"],
            "L": ["UUA", "UUG", "CUU", "CUC", "CUA", "CUG"],
            "S": ["UCU", "UCC", "UCA", "UCG", "AGU", "AGC"],
            "Y": ["UAU", "UAC"],
            "Stop": ["UAA", "UAG", "UGA"],
            "C": ["UGU", "UGC"],
            "W": ["UGG"],
            "P": ["CCU", "CCC", "CCA", "CCG"],
            "H": ["CAU", "CAC"],
            "Q": ["CAA", "CAG"],
            "R": ["CGU", "CGC", "CGA", "CGG", "AGA", "AGG"],
            "I": ["AUU", "AUC", "AUA"],
            "M": ["AUG"],
            "T": ["ACU", "ACC", "ACA", "ACG"],
            "N": ["AAU", "AAC"],
            "K": ["AAA", "AAG"],
            "V": ["GUU", "GUC", "GUA", "GUG"],
            "A": ["GCU", "GCC", "GCA", "GCG"],
            "D": ["GAU", "GAC"],
            "E": ["GAA", "GAG"],
            "G": ["GGU", "GGC", "GGA", "GGG"],
        }

        self.monoisotopic_mass_table = {
            "A": 71.03711,
            "C": 103.00919,
            "D": 115.02694,
            "E": 129.04259,
            "F": 147.06841,
            "G": 57.02146,
            "H": 137.05891,
            "I": 113.08406,
            "K": 128.09496,
            "L": 113.08406,
            "M": 131.04049,
            "N": 114.04293,
            "P": 97.05276,
            "Q": 128.05858,
            "R": 156.10111,
            "S": 87.03203,
            "T": 101.04768,
            "V": 99.06841,
            "W": 186.07931,
            "Y": 163.06333,
        }

    def translate_codon(self, codon: str) -> str:
        """Returns the amino acid that corresponds to the given RNA codon."""
        return self.rna_codon_table[codon]

    def get_codons(self, amino_acid: str) -> list:
        """Returns a list of codons that code for the given amino acid."""
        return self.reverse_codon_table[amino_acid]

    def translate(self, messenger_rna: str) -> str:
        """Translates given mRNA strand into protein chain,
        starting from the first start codon encountered."""

        protein_chain = ""
        orf = messenger_rna[messenger_rna.find("AUG") :]

        for index in range(0, len(orf), 3):
            codon = orf[index : index + 3]
            if codon in self.reverse_codon_table["Stop"]:
                break
            protein_chain += self.translate_codon(codon)

        return protein_chain


def read_fasta(sequences: str = None, file_path: str = None) -> dict:
    """
    Returns sequences in FASTA format as dictionary
    with key-value pairs of name to sequence.

    Args:
        sequences (str): Sequences in FASTA format
        file_path (str): Path to FASTA file

    Returns:
        dict: Key-value pairs of name to sequence
    """

    reads = {}

    if sequences is not None:
        lines = sequences.splitlines()
    elif file_path is not None:
        with open(file_path, "r") as file:
            lines = file.read().splitlines()
    else:
        raise Exception("Error: No FASTA sequences given")

    header = lines[0]

    for line in lines:
        if line.startswith(">"):
            header = line
            reads[header] = ""
            continue
        reads[header] += line

    return reads


def get_reads(fasta_file: str) -> dict:
    """Reads sequences from FASTA file"""
    return read_fasta(file_path=fasta_file)


def generate_profile_matrix(reads: list) -> dict:
    """
    Generates profile matrix with shape 4 x n for
    collection of DNA strands with length n.

    Args:
        reads (dict): Dictionary with key-value pairs of
        read titles and DNA strands from a FASTA file.

    Returns:
        dict: 4 x n profile matrix for given DNA strands.
    """

    profile_matrix = {
        "A": [0 for nt in reads[0]],
        "C": [0 for nt in reads[0]],
        "G": [0 for nt in reads[0]],
        "T": [0 for nt in reads[0]],
    }

    for index in range(len(reads[0])):
        for read in reads:
            profile_matrix[read[index]][index] += 1

    return profile_matrix


def get_consensus(profile_matrix: dict) -> str:
    """
    Returns first consensus strand found from the given profile matrix.

    Args:
        profile_matrix (dict): Profile matrix of dimension 4 x n,
        with nucleotide occurrences in each strand of length n.

    Returns:
        str: Consensus strand
    """

    consensus_strand = ""
    length = len(profile_matrix["A"])

    for index in range(length):
        nt = "-"
        max = 0
        for key in profile_matrix.keys():
            occurrences = profile_matrix[key][index]
            if occurrences > max:
                max = occurrences
                nt = key
        consensus_strand += nt

    return consensus_strand


def reverse_complement(dna: str) -> str:
    """
    Returns the reverse complement of a given DNA strand.
    """

    complementary_stand = ""
    complements = {"A": "T", "T": "A", "G": "C", "C": "G"}
    for nt in reversed(dna):
        complementary_stand += complements[nt]
    return complementary_stand
