from rdworks import IonizedStates


def test_ionizedstate():    
    smiles = 'O=C(NCCCC)[C@H](CCC1)N1[C@@H](CC)C2=NN=C(CC3=CC=C(C)C=C3)O2'
    x = IonizedStates(smiles)

    assert x.count() == 7
    
    d = x.get_sites()
    print('sites:')
    for k, v in d.items():
        print(k, v)
    print()

    indices = d['CCCCNC(=O)[C@@H]1CCCN1[C@@H](CC)c1nnc(Cc2ccc(C)cc2)o1'][0]
    
    assert (11, 'B') in indices
    assert (16, 'B') in indices
    assert (17, 'B') in indices

    expected = ['CCCCNC(=O)[C@@H]1CCCN1[C@@H](CC)c1nnc(Cc2ccc(C)cc2)o1', 
                'CCCCNC(=O)[C@@H]1CCCN1[C@@H](CC)c1[nH+]nc(Cc2ccc(C)cc2)o1', 
                'CCCCNC(=O)[C@@H]1CCC[NH+]1[C@@H](CC)c1nnc(Cc2ccc(C)cc2)o1', 
                'CCCCNC(=O)[C@@H]1CCCN1[C@@H](CC)c1n[nH+]c(Cc2ccc(C)cc2)o1', 
                'CCCCNC(=O)[C@@H]1CCC[NH+]1[C@@H](CC)c1[nH+]nc(Cc2ccc(C)cc2)o1', 
                'CCCCNC(=O)[C@@H]1CCCN1[C@@H](CC)c1[nH+][nH+]c(Cc2ccc(C)cc2)o1', 
                'CCCCNC(=O)[C@@H]1CCC[NH+]1[C@@H](CC)c1n[nH+]c(Cc2ccc(C)cc2)o1']
    results = x.get_smiles()
    assert set(expected).intersection(set(results)) == set(expected)


if __name__ == '__main__':
    test_ionizedstate()