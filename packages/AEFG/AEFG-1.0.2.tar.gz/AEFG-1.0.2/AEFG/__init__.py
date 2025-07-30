

import re
import copy
import pandas as pd
from rdkit import Chem
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.warning')

from rdkit.Chem import AllChem
from rdkit.Chem import DataStructs
from rdkit.Chem.Draw import rdMolDraw2D
from IPython.display import SVG


def is_amide_n_bond(mol, c_idx, n_idx):
        
        c_atom = mol.GetAtomWithIdx(c_idx)
        n_atom = mol.GetAtomWithIdx(n_idx)
        # print(n_atom)
        bond_cn = mol.GetBondBetweenAtoms(c_idx, n_idx)

        
        if bond_cn and bond_cn.GetBondTypeAsDouble() == 1.0:
           
            for neighbor in n_atom.GetNeighbors():
                if neighbor.GetSymbol() == 'C':  
                    amide_c_idx = neighbor.GetIdx()
                    n_atom_amide = mol.GetAtomWithIdx(amide_c_idx)
              
                    for neighbor in n_atom_amide.GetNeighbors():
                        if neighbor.GetSymbol() == 'O':
                            # print(neighbor.GetSymbol())
                            bond_co = mol.GetBondBetweenAtoms(amide_c_idx, neighbor.GetIdx())
                            if bond_co and bond_co.GetBondTypeAsDouble() == 2.0:  
                               
                                return True
        return False


def is_amide_c_bond(mol, c_idx):
    
    c_atom = mol.GetAtomWithIdx(c_idx)

    has_n_single_bond = False
    for neighbor in c_atom.GetNeighbors():
        if neighbor.GetSymbol() == 'N':
            bond_cn = mol.GetBondBetweenAtoms(c_idx, neighbor.GetIdx())
            if bond_cn and bond_cn.GetBondTypeAsDouble() == 1.0:
                has_n_single_bond = True
                break

    has_o_double_bond = False
    for neighbor in c_atom.GetNeighbors():
        if neighbor.GetSymbol() == 'O':
            bond_co = mol.GetBondBetweenAtoms(c_idx, neighbor.GetIdx())
            if bond_co and bond_co.GetBondTypeAsDouble() == 2.0:
                has_o_double_bond = True
                break

    return has_o_double_bond and has_n_single_bond


def is_amide_o_bond(mol, c_idx, o_idx):
  
    c_atom = mol.GetAtomWithIdx(c_idx)
    n_atom = mol.GetAtomWithIdx(o_idx)
   
    bond_cn = mol.GetBondBetweenAtoms(c_idx, o_idx)

    if bond_cn and bond_cn.GetBondTypeAsDouble() == 1.0:
       
        for neighbor in n_atom.GetNeighbors():
            if neighbor.GetSymbol() == 'C' and neighbor.GetIdx() != c_idx:    
                amide_c_idx = neighbor.GetIdx()
                # print(amide_c_idx)
                n_atom_amide = mol.GetAtomWithIdx(amide_c_idx)
                
                for neighbor in n_atom_amide.GetNeighbors():
                    if neighbor.GetSymbol() == 'N'and not neighbor.IsInRing():
                        # print(neighbor.GetIdx())
                        bond_co = mol.GetBondBetweenAtoms(amide_c_idx, neighbor.GetIdx())
                        if bond_co and bond_co.GetBondTypeAsDouble() == 1.0:  
                            
                            n_atom_amide_2 = mol.GetAtomWithIdx(amide_c_idx)
                            for neighbor in n_atom_amide_2.GetNeighbors():

                                if neighbor.GetSymbol() == 'O' :
                                  
                                    bond_co = mol.GetBondBetweenAtoms(amide_c_idx, neighbor.GetIdx())
                                    if bond_co and bond_co.GetBondTypeAsDouble() == 2.0: 
                                    
                                        return True
                            
    return False


def is_s_c_bond(mol, c_idx):
    
    c_atom = mol.GetAtomWithIdx(c_idx)

    
    has_n_single_bond = False
    for neighbor in c_atom.GetNeighbors():
        if neighbor.GetSymbol() == 'S':
            bond_cn = mol.GetBondBetweenAtoms(c_idx, neighbor.GetIdx())
            if bond_cn and bond_cn.GetBondTypeAsDouble() == 1.0:
                has_n_single_bond = True
                break

    has_o_double_bond = False
    for neighbor in c_atom.GetNeighbors():
        if neighbor.GetSymbol() == 'O':
            bond_co = mol.GetBondBetweenAtoms(c_idx, neighbor.GetIdx())
            if bond_co and bond_co.GetBondTypeAsDouble() == 2.0:
                has_o_double_bond = True
                break

    return has_o_double_bond and has_n_single_bond


def is_s_double_o_bond(mol, c_idx, s_idx):
   
    c_atom = mol.GetAtomWithIdx(c_idx)
    s_atom = mol.GetAtomWithIdx(s_idx)

   
    bond_cs = mol.GetBondBetweenAtoms(c_idx, s_idx)
    if bond_cs and bond_cs.GetBondTypeAsDouble() == 1.0: 
      
        double_bond_oxygens = 0
        for neighbor in s_atom.GetNeighbors():
            if neighbor.GetSymbol() == 'O':
                bond_so = mol.GetBondBetweenAtoms(s_idx, neighbor.GetIdx())
                if bond_so and bond_so.GetBondTypeAsDouble() == 2.0: 
                    double_bond_oxygens += 1
        
        if double_bond_oxygens == 2:
            return True

    return False


def is_three_n_c_bond(mol, c_idx):

    c_atom = mol.GetAtomWithIdx(c_idx)

    if c_atom.GetSymbol() == 'C' and not c_atom.IsInRing():
        
        neighbors = c_atom.GetNeighbors()
        
        
        n_count = sum(1 for neighbor in neighbors if neighbor.GetSymbol() == 'N' and not neighbor.IsInRing())
        
        if n_count == 3:
            return True

    return False


def is_three_n_bond(mol, c_idx, n_idx):
   
    c_atom = mol.GetAtomWithIdx(c_idx)
    n_atom = mol.GetAtomWithIdx(n_idx)

    if c_atom.GetSymbol() == 'C' and n_atom.GetSymbol() == 'N' :
    
        if n_atom is not n_atom.IsInRing():
     
            for neighbor in n_atom.GetNeighbors():
                if neighbor.GetSymbol() == 'C' and neighbor.GetIdx() != c_idx:
              
                    n_neighbors = [
                        neigh for neigh in neighbor.GetNeighbors()
                        if neigh.GetSymbol() == 'N' and not neigh.IsInRing()
                    ]
            
                    if len(n_neighbors) == 3:
                        return True

    return False


def double_bond_c(mol, c_idx, o_idx):
  
    c_atom = mol.GetAtomWithIdx(c_idx)
    o_atom = mol.GetAtomWithIdx(o_idx)

    for neighbor in c_atom.GetNeighbors():
        if neighbor.GetSymbol() == 'C':  
            bond_cn = mol.GetBondBetweenAtoms(c_idx, neighbor.GetIdx())
            if bond_cn and bond_cn.GetBondTypeAsDouble() == 2.0:  
                
              
                bond_co = mol.GetBondBetweenAtoms(c_idx, o_idx)
                if bond_co and bond_co.GetBondTypeAsDouble() == 1.0:  

                
                    for o_neighbor in o_atom.GetNeighbors():
                        if o_neighbor.GetSymbol() == 'O':  
                            bond_oo = mol.GetBondBetweenAtoms(o_idx, o_neighbor.GetIdx())
                            if bond_oo and bond_oo.GetBondTypeAsDouble() == 1.0: 
                                return True

    
    return False


def get_carbon_environments(mol):
    
    carbon_environments = []
    # Step 1: Identify aromatic atoms and handle aromatic rings
    mol_ring = copy.deepcopy(mol)
    aromatic_atoms = set() 
    Chem.GetSymmSSSR(mol_ring)  # Find rings
    rings = mol_ring.GetRingInfo().AtomRings()

    for ring in rings:
        ring_atoms = set(ring)
        # aromatic_atoms.update(ring_atoms)  
        ring_smiles = Chem.MolFragmentToSmiles(mol_ring, atomsToUse=ring_atoms)
        ring_atom_indices = ','.join(map(str, sorted(ring_atoms)))
        ring_string = f"{ring_smiles}:{ring_atom_indices}|{ring_smiles}:{ring_atom_indices}"
        carbon_environments.append(ring_string)

        aromatic_ring = all(mol_ring.GetAtomWithIdx(atom_idx).GetIsAromatic() for atom_idx in ring)
        if aromatic_ring:  # Handle aromatic rings
            aromatic_atoms.update(ring_atoms)

    
    def find_fused_rings(rings):
       
        fused_rings_list = []
        visited = set()  

        for i, ring1 in enumerate(rings):
            if i in visited:
                continue  

            # fused_set
            fused_set = set(ring1)
            queue = [i] 

            while queue:
                current_idx = queue.pop(0)
                visited.add(current_idx)

                for j, ring2 in enumerate(rings):
                    if j in visited:
                        continue
                    if fused_set.intersection(ring2): 
                        fused_set.update(ring2)
                        queue.append(j)  

            fused_rings_list.append(fused_set)

        return fused_rings_list

    carbon_environments = []
    
    # Step 1
    mol_ring = copy.deepcopy(mol)
    aromatic_atoms = set()  
    Chem.GetSymmSSSR(mol_ring)  
    rings = mol_ring.GetRingInfo().AtomRings()  

    # Step 2
    for ring in rings:
        ring_atoms = set(ring)
        ring_smiles = Chem.MolFragmentToSmiles(mol_ring, atomsToUse=ring_atoms)
        ring_atom_indices = ','.join(map(str, sorted(ring_atoms)))
        ring_string = f"{ring_smiles}:{ring_atom_indices}|{ring_smiles}:{ring_atom_indices}"
        carbon_environments.append(ring_string)

      
        aromatic_ring = all(mol_ring.GetAtomWithIdx(atom_idx).GetIsAromatic() for atom_idx in ring)
        if aromatic_ring:
            aromatic_atoms.update(ring_atoms) 

    # Step 3
    fused_rings_list = find_fused_rings(rings)
    for fused_rings in fused_rings_list:
        fused_smiles = Chem.MolFragmentToSmiles(mol_ring, atomsToUse=list(fused_rings))
        fused_atom_indices = ','.join(map(str, sorted(fused_rings)))
        carbon_environments.append(f"{fused_smiles}:{fused_atom_indices}|{fused_smiles}:{fused_atom_indices}")

       
        aromatic_fused_ring = all(mol_ring.GetAtomWithIdx(atom_idx).GetIsAromatic() for atom_idx in fused_rings)
        if aromatic_fused_ring:
            aromatic_atoms.update(fused_rings) 
    

    # Step 2: Handle atom environment(Skip aromatic atoms)
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 6:
            atom_idx = atom.GetIdx()
            if atom_idx in aromatic_atoms:  # Skip aromatic atoms
                continue
            
            # Find C atom environment
            env_bond_indices = Chem.FindAtomEnvironmentOfRadiusN(mol, 1, atom_idx)
            if env_bond_indices:
                env = Chem.PathToSubmol(mol, env_bond_indices)
                AllChem.AssignStereochemistry(env, cleanIt=True, force=True)
                env_smiles_all = Chem.MolToSmiles(env, isomericSmiles=True) 
                
                env_atom_indices = sorted(set([atom_idx for bond_idx in env_bond_indices for atom_idx in (
                                mol.GetBondWithIdx(bond_idx).GetBeginAtomIdx(), mol.GetBondWithIdx(bond_idx).GetEndAtomIdx())]))
            
                env_atom_indices.remove(atom_idx)
                env_atom_indices.insert(0, atom_idx) 
                
                # Filter neighbors
                neighbors = [] 
                for neighbor in mol.GetAtomWithIdx(atom_idx).GetNeighbors():
                    
                    neighbor_idx = neighbor.GetIdx()
                    bond = mol.GetBondBetweenAtoms(atom_idx, neighbor_idx)
                  
                    if neighbor.GetSymbol() != 'C' or bond.GetBondTypeAsDouble() != 1.0 : 
                      
                        if (neighbor.GetSymbol() not in ['N', 'S', 'P','C','O']) or \
                            (neighbor.GetSymbol() == 'N' and not neighbor.IsInRing()) or \
                            (neighbor.GetSymbol() == 'S' and not neighbor.IsInRing()) or \
                            (neighbor.GetSymbol() == 'P' and not neighbor.IsInRing()) or \
                            (neighbor.GetSymbol() == 'C' and not neighbor.IsInRing()) or \
                            (neighbor.GetSymbol() == 'O' and not neighbor.IsInRing()):
                            
                            if not (is_amide_c_bond(mol, atom_idx)):
                               
                                if  (is_amide_n_bond(mol, atom_idx, neighbor_idx)):
                                    # print(neighbor_idx)
                            
                                    if neighbor.GetSymbol() == 'N':
                                        continue
                            if  (is_amide_o_bond(mol, atom_idx, neighbor_idx)):
                                # print(neighbor_idx)
                                if neighbor.GetSymbol() == 'O' and  is_amide_n_bond(mol, atom_idx, neighbor_idx):
                                    continue


                            if not (is_three_n_c_bond(mol, atom_idx)):
                                # print(atom_idx)
                                if (is_three_n_bond(mol, atom_idx, neighbor_idx)):
                                    # print(neighbor_idx)
                                    # if neighbor.GetSymbol() == 'N':
                                    if neighbor.GetSymbol() == 'N' and not is_amide_n_bond(mol, atom_idx, neighbor_idx):
                                        continue

                            if (double_bond_c(mol, atom_idx, neighbor_idx)):
                                if neighbor.GetSymbol() == 'O':
                                        continue

                            if not (is_s_c_bond(mol, atom_idx)):
                                # print(atom_idx)
                                if  (is_amide_n_bond(mol, atom_idx, neighbor_idx)): 
                               
                                    if neighbor.GetSymbol() == 'S':
                                        continue
                            if  (is_s_double_o_bond(mol, atom_idx, neighbor_idx)):      
                                if neighbor.GetSymbol() == 'S' :
                                 
                                    continue

                            neighbors.append(neighbor_idx)
            
                # Create submol
                submol = Chem.RWMol(mol)
                atom_map = {}
          
                for idx in neighbors + [atom_idx]:
                    new_atom = submol.AddAtom(mol.GetAtomWithIdx(idx))
                    atom_map[idx] = new_atom
                
                for idx in neighbors + [atom_idx]:
                    for neighbor in mol.GetAtomWithIdx(idx).GetNeighbors():
                        if neighbor.GetIdx() in atom_map and idx < neighbor.GetIdx():
                            submol.AddBond(atom_map[idx], atom_map[neighbor.GetIdx()], mol.GetBondBetweenAtoms(idx, neighbor.GetIdx()).GetBondType())
                env_smiles = Chem.MolFragmentToSmiles(submol, atomsToUse=list(atom_map.values()), isomericSmiles=True, allHsExplicit=False, kekuleSmiles=False)

                env_string = f"{env_smiles}:{atom_idx},{','.join(map(str, neighbors))}|{env_smiles_all}:{','.join(map(str, env_atom_indices))}"

                env_string = env_string.replace(',:', ':').replace(',|', '|')
                carbon_environments.append(env_string)
   
    # Step 3 

    def filter_subsmiles(carbon_environments):
        # Step 1: Parse entries
        parsed_entries = {}
        for entry in carbon_environments:
            subsmiles, numbers = entry.split("|")[0].rsplit(":", 1)
            num_list = set(map(int, numbers.split(",")))
            parsed_entries[entry] = num_list

        # Step 2: Remove duplicates, keeping the entry with the larger set
        unique_entries = {}
        for key, value in parsed_entries.items():
            is_unique = True
            keys_to_remove = []
            for unique_key, unique_value in unique_entries.items():
                if value.issubset(unique_value):
                    is_unique = False
                    break
                elif unique_value.issubset(value):
                    keys_to_remove.append(unique_key)
            if is_unique:
                unique_entries[key] = value
            for k in keys_to_remove:
                del unique_entries[k]
        return list(unique_entries.keys())
    unique_keys = filter_subsmiles(carbon_environments)


    def update_unique_keys(unique_keys, mol):
        """
        Update the unique_keys list by removing certain atom indices and replacing 'OC=O' with 'C=O'.
        """
      
        for idx, i in enumerate(unique_keys):
            front_part, back_part = i.split('|')
            o_id = front_part.split(":")[-1]
            group = front_part.split(":")[0]
            if group == 'OC=O':
                o_indices = list(map(int, o_id.split(','))) 

                new_indices = []
                for atom_idx in o_indices:
                    atom = mol.GetAtomWithIdx(atom_idx)
                    if atom.GetAtomicNum() == 8:  
                        has_double_bond = False
                        has_hydrogen = False

                      
                        for neighbor in atom.GetNeighbors():
                            bond = mol.GetBondBetweenAtoms(atom_idx, neighbor.GetIdx())
                            if bond.GetBondTypeAsDouble() == 2.0:  
                                has_double_bond = True
                            if neighbor.GetAtomicNum() == 1:  
                                has_hydrogen = True

                      
                        if has_double_bond or has_hydrogen:
                            new_indices.append(atom_idx)
                    else:
                        new_indices.append(atom_idx)

              
                if new_indices != o_indices:
                    new_id = ','.join(map(str, new_indices))
                    modified_front_part = front_part.replace('OC=O', 'C=O').replace(o_id, new_id)
                    modified_group = f"{modified_front_part}|{back_part}"

              
                    unique_keys[idx] = modified_group

        return unique_keys
    
    updated_unique_keys = update_unique_keys(unique_keys, mol)
    
    return updated_unique_keys


def is_amide_bond(mol, atom_idx):
 
    atom = mol.GetAtomWithIdx(atom_idx)
    atom_symbol = atom.GetSymbol()


    if atom_symbol == 'N':
   
        for neighbor in atom.GetNeighbors():
      
            if neighbor.GetSymbol() == 'C':
                for second_neighbor in neighbor.GetNeighbors():
                    if second_neighbor.GetSymbol() == 'O':
                        # print(f"{atom_idx} (N) is amide bond")
                        return True  

    elif atom_symbol == 'O' and not atom.IsInRing():
     
        for neighbor in atom.GetNeighbors():
           
            if neighbor.GetSymbol() == 'C':
                for second_neighbor in neighbor.GetNeighbors():
                    if second_neighbor.GetSymbol() == 'N' and not second_neighbor.IsInRing():
                        # print(f"{atom_idx} (O) is amide bond")
                        return True 

    return False  


def is_amide_s_bond(mol, atom_idx):
    
    atom = mol.GetAtomWithIdx(atom_idx)
    atom_symbol = atom.GetSymbol()

    if atom_symbol == 'S':
     
        for neighbor in atom.GetNeighbors():

            if neighbor.GetSymbol() == 'C':
                for second_neighbor in neighbor.GetNeighbors():
                    if second_neighbor.GetSymbol() == 'O':
                        # print(f"{atom_idx} (S) is amide bond")
                        return True 

    elif atom_symbol == 'O' and not atom.IsInRing():
    
        for neighbor in atom.GetNeighbors():
        
            if neighbor.GetSymbol() == 'C':
                for second_neighbor in neighbor.GetNeighbors():
                    if second_neighbor.GetSymbol() == 'S' and not second_neighbor.IsInRing():
                        # print(f"{atom_idx} (O) is amide bond")
                        return True  

    return False  


def is_tren_bond(mol, atom_idx):
   
    atom = mol.GetAtomWithIdx(atom_idx)
    atom_symbol = atom.GetSymbol()

    if atom_symbol == 'N' and not atom.IsInRing():  
        for neighbor in atom.GetNeighbors():
           
            if neighbor.GetSymbol() == 'C':
              
                carbon_neighbors = neighbor.GetNeighbors()
               
                n_count = sum(
                    1
                    for second_neighbor in carbon_neighbors
                    if second_neighbor.GetSymbol() == 'N' and not second_neighbor.IsInRing()
                )

        
                if n_count == 3:
                    # print(f"Atom {atom_idx} (N) is part of a TREN bond (excluding ring N)")
                    return True

    return False 


def get_non_carbon_environment(mol, atom_idx):

    visited_atoms = set()
    env_atoms = set([atom_idx])
    ring_info = mol.GetRingInfo()
    
    def recurse(atom_idx):
        atom = mol.GetAtomWithIdx(atom_idx)
        visited_atoms.add(atom_idx)
        for neighbor in atom.GetNeighbors():
            neighbor_idx = neighbor.GetIdx()
          
            if any(neighbor_idx in ring for ring in ring_info.AtomRings()): 
                env_atoms.add(neighbor_idx)
                continue
            if neighbor_idx not in visited_atoms:
                if neighbor.GetSymbol() == 'C':
                    env_atoms.add(neighbor_idx)
                
                else:
                    env_atoms.add(neighbor_idx)
                    recurse(neighbor_idx)
    
    recurse(atom_idx)
    
    env_bonds = set()
    for atom_idx in env_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        for bond in atom.GetBonds():
            begin_idx = bond.GetBeginAtomIdx()
            end_idx = bond.GetEndAtomIdx()
            if begin_idx in env_atoms and end_idx in env_atoms:
                env_bonds.add(bond.GetIdx())
    
    env = Chem.PathToSubmol(mol, list(env_bonds))
    AllChem.AssignStereochemistry(env, cleanIt=True, force=True, flagPossibleStereoCenters=True)
    env_smiles = Chem.MolToSmiles(env, isomericSmiles=True)

    env_atom_indices = sorted(env_atoms)
    env_atom_indices.remove(atom_idx)
    env_atom_indices.insert(0, atom_idx)
    
    env_string = f"{env_smiles}:{','.join(map(str, env_atom_indices))}"

    return env_string


def get_non_carbon_atom_environments(mol):
    non_carbon_environments = []
    aromatic_atoms = set()
    Chem.GetSymmSSSR(mol)  
    rings = mol.GetRingInfo().AtomRings()
    for ring in rings:
        ring_atoms = set(ring)
        aromatic_atoms.update(ring_atoms)
    
    for atom in mol.GetAtoms():
        atom_idx = atom.GetIdx()
        atom_symbol = atom.GetSymbol()

        if atom_symbol == 'C' or atom_idx in aromatic_atoms: 
            continue 

        if atom_symbol == 'N' and is_amide_bond(mol, atom_idx) or is_tren_bond(mol, atom_idx):
            continue  

        if atom_symbol == 'O' and is_amide_bond(mol, atom_idx):
            continue  

        if atom_symbol == 'S' and  is_amide_s_bond(mol, atom_idx):
            continue  
        
        env_string = get_non_carbon_environment(mol, atom_idx)
        non_carbon_environments.append(env_string)
    
    return set(non_carbon_environments)


def merge_environments(carbon_env, non_carbon_env):
    # First, filter out elements from carbon_env that have subsets in non_carbon_env
    filtered_carbon_env = set()
    for c_env in carbon_env:
        c_smiles, c_indices_str = c_env.split('|')
        c_indices = set(c_indices_str.split(':')[1].split(','))
        
        keep = True
        for nc_env in non_carbon_env:
            nc_indices = set(nc_env.split(':')[1].split(','))
            if c_indices.issubset(nc_indices):
                keep = False
                break
        if keep:
            filtered_carbon_env.add(c_env)
    
    # Then, filter out elements from non_carbon_env that have subsets in the remaining carbon_env
    filtered_non_carbon_env = []
    for nc_env in non_carbon_env:
        nc_indices = set(nc_env.split(':')[1].split(','))
        
        keep = True
        for c_env in filtered_carbon_env:
            c_smiles, c_indices_str = c_env.split('|')
            c_indices = set(c_indices_str.split(':')[1].split(','))
            if nc_indices.issubset(c_indices):
                keep = False
                break
        if keep:
            filtered_non_carbon_env.append(nc_env)
    
    # Finally, add the filtered non_carbon_env to the filtered_carbon_env
    merged_env = filtered_carbon_env.union(filtered_non_carbon_env)
    
  
    def merge_env_new(env_list):
        merged_env = set(env_list)
        for item in env_list:
            if "|" in item:
                nums1 = set(item.split("|")[0].split(":")[1].split(","))
                for x in merged_env.copy():
                    if "|" not in x:
                        nums2 = set(x.split(":")[1].split(","))
                        if nums1.issubset(nums2) and len(nums1) < len(nums2):
                            merged_env.discard(item)
                            break
        return merged_env
    
    
    def get_sort_key(item):
        if "|" in item:

            key_part = item.split("|")[1]
            key_num = int(key_part.rsplit(":",1)[1].split(",")[0]) 
        else:
            key_num = int(item.rsplit(":",1)[1].split(",")[0]) 
        return key_num
    

    def filter_unique_elements(merged_env):

        unique_elements = {}

        for item in merged_env:
       
            key, value = item.rsplit(':', 1)
            numbers = tuple(map(int, value.split(',')))
            sorted_numbers = tuple(sorted(numbers))

            if (key, sorted_numbers) not in unique_elements or min(numbers) < unique_elements[(key, sorted_numbers)]:
                unique_elements[(key, sorted_numbers)] = min(numbers)
                unique_elements[(key, sorted_numbers, 'original')] = item

        result = [unique_elements[k] for k in unique_elements if 'original' in k]
        return result
    
   
    def process_merged_env(env_list):
 
        parsed_env = [
            (entry.split(":")[0], list(map(int, entry.split(":")[1].split(",")))) for entry in env_list
        ]
        
        # print(parsed_env)
   
        removed_indices = set()
        
        result = []

        for i, (smiles_a, indices_a) in enumerate(parsed_env):
            if i in removed_indices:
                continue  

            should_remove = False 

            
            for j, (smiles_b, indices_b) in enumerate(parsed_env):
                if i == j or j in removed_indices:
                    continue  

                
                if indices_a[0] in indices_b:
                  
                    remaining_indices_found = all(
                        any(idx in indices_c for k, (_, indices_c) in enumerate(parsed_env) if k != i and k not in removed_indices)
                        for idx in indices_a[1:]
                    )
                    if remaining_indices_found:
                        should_remove = True
                        removed_indices.add(i)  
                        break

            if not should_remove:
           
                result.append(f"{smiles_a}:{','.join(map(str, indices_a))}")

        return result


   
    merged_env_new = merge_env_new(merged_env)
    merged_env_new = sorted(merged_env_new, key=get_sort_key)

    merged_env_new = [item.split("|")[0] if "|" in item else item for item in merged_env_new]
    merged_env_new = filter_unique_elements(merged_env_new)
    # print(merged_env_new)
    processed_env = process_merged_env(merged_env_new)

    return processed_env


def rxn_fg(rxn_smiles):
  
    rea = rxn_smiles.split('>>')[0].split('.')
    pro = rxn_smiles.split('>>')[1].split('.')

    r_atom_env = []
    for r in rea:
        r_mol = Chem.MolFromSmiles(r)

     
        carbon_env = get_carbon_environments(r_mol)
        non_carbon_env = get_non_carbon_atom_environments(r_mol) # get_non_carbon_atom_environments
        atom_env = merge_environments(carbon_env, non_carbon_env)
     
        if atom_env ==[':0']:
            atom_env = []
        if atom_env :
        
            atom_env_cleaned = [item.rsplit(':',1 )[0] for item in atom_env] 
            r_atom_env.extend(atom_env_cleaned)
        else:         
        
            atom_env_cleaned = [Chem.MolToSmiles(r_mol)]
            r_atom_env.extend(atom_env_cleaned)
        r_atom_env.append('.')
    
    if r_atom_env:
        r_atom_env.pop()

    p_atom_env = []
    for p in pro:
        p_mol = Chem.MolFromSmiles(p)
   
        carbon_env = get_carbon_environments(p_mol)
        non_carbon_env = get_non_carbon_atom_environments(p_mol) # get_non_carbon_atom_environments
        atom_env = merge_environments(carbon_env, non_carbon_env)
        if atom_env ==[':0']:
            atom_env = []
        if atom_env :
         
            atom_env_cleaned = [item.rsplit(':',1 )[0] for item in atom_env]
            p_atom_env.extend(atom_env_cleaned)
        else:
            atom_env_cleaned = [Chem.MolToSmiles(p_mol)]
            p_atom_env.extend(atom_env_cleaned)
        p_atom_env.append('.')
    
    if p_atom_env:
        p_atom_env.pop()

    r_atom_env.extend(['>>'])
    r_atom_env.extend(p_atom_env)
    return r_atom_env


def molecule_fg(smiles):

    r_mol = Chem.MolFromSmiles(smiles)
    carbon_env = get_carbon_environments(r_mol)
    non_carbon_env = get_non_carbon_atom_environments(r_mol) 
    atom_env = merge_environments(carbon_env, non_carbon_env)

    return atom_env


if __name__ == "__main__":
  
    rxn_smlies= 'N[C@@H](CC(=O)O)C(=O)O.O=C(O)CCC(=O)C(=O)O>>N[C@H](CCC(=O)O)C(=O)O.O=C(O)CC(=O)C(=O)O'
    rxn_fp = rxn_fg(rxn_smlies)
    print(rxn_fp)