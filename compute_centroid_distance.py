import argparse
import numpy as np
import mdtraj as md
import pandas as pd
import matplotlib.pyplot as plt
import os

def compute_centroid_distance(topology_file, trajectory_file, ligand_selection, pocket_selection, output_csv, output_plot):
    print(f"Loading topology: {topology_file}")
    print(f"Loading trajectory: {trajectory_file}")
    
    # Load trajectory using MDTraj
    # MDTraj can automatically detect .dtr directories and load them if topology is provided
    try:
        t = md.load(trajectory_file, top=topology_file)
    except Exception as e:
        print(f"Failed to load with md.load: {e}")
        print("Attempting to load explicitly as DTR...")
        t = md.load_dtr(trajectory_file, top=topology_file)
        
    print(f"Successfully loaded {t.n_frames} frames.")
    
    # Select heavy atoms (excluding Hydrogens)
    lig_atoms = t.topology.select(f"({ligand_selection}) and symbol != H")
    poc_atoms = t.topology.select(f"({pocket_selection}) and symbol != H")
    
    if len(lig_atoms) == 0:
        raise ValueError(f"Ligand selection '{ligand_selection}' found 0 heavy atoms. Please check your selection string.")
    if len(poc_atoms) == 0:
        raise ValueError(f"Pocket selection '{pocket_selection}' found 0 heavy atoms. Please check your selection string.")
        
    print(f"Selected {len(lig_atoms)} ligand heavy atoms and {len(poc_atoms)} pocket heavy atoms.")
    
    # Extract Coordinates
    # t.xyz has shape (n_frames, n_atoms, 3) and is in nanometers
    lig_xyz = t.xyz[:, lig_atoms, :] 
    poc_xyz = t.xyz[:, poc_atoms, :]
    
    # Compute geometric centroids (average position of all heavy atoms in the selection)
    lig_centroid = np.mean(lig_xyz, axis=1) # shape (n_frames, 3)
    poc_centroid = np.mean(poc_xyz, axis=1)
    
    # Compute Euclidean distance between the two centroids
    distances_nm = np.linalg.norm(lig_centroid - poc_centroid, axis=1)
    
    # Convert distances from nanometers (MDTraj default) to Angstroms
    distances_angstrom = distances_nm * 10.0
    
    # Time array (MDTraj time is in picoseconds, convert to nanoseconds)
    times_ns = t.time / 1000.0 
    
    # Save the time series data to a CSV file
    df = pd.DataFrame({
        'Time_ns': times_ns,
        'Distance_Angstrom': distances_angstrom
    })
    df.to_csv(output_csv, index=False)
    print(f"Saved distance time series to {os.path.abspath(output_csv)}")
    
    # Generate a Publication-Quality Plot
    plt.figure(figsize=(10, 6))
    plt.plot(times_ns, distances_angstrom, color='teal', linewidth=1.5)
    
    plt.xlabel('Time (ns)', fontsize=14, fontweight='bold')
    plt.ylabel('Centroid Distance (Å)', fontsize=14, fontweight='bold')
    plt.title('Ligand-to-Pocket Centroid Distance Time Series', fontsize=16, fontweight='bold')
    
    # Format axes and grid
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    # Add a horizontal line for the mean distance
    mean_dist = np.mean(distances_angstrom)
    plt.axhline(mean_dist, color='red', linestyle='--', linewidth=2, label=f'Mean = {mean_dist:.2f} Å')
    plt.legend(fontsize=12)
    
    plt.tight_layout()
    plt.savefig(output_plot, dpi=300, bbox_inches='tight')
    print(f"Saved publication-quality plot to {os.path.abspath(output_plot)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute Ligand-to-Pocket Centroid Distance Time Series for MD Complexes")
    parser.add_argument("-p", "--topology", required=True, help="Path to topology file (e.g., .pdb, .cms)")
    parser.add_argument("-t", "--trajectory", required=True, help="Path to trajectory file or directory (e.g., .dtr)")
    parser.add_argument("-l", "--ligand", default="resname UNK", help="MDTraj selection string for the ligand")
    parser.add_argument("-r", "--pocket", required=True, help="MDTraj selection string for pocket residues (e.g., 'resSeq 10 to 20')")
    parser.add_argument("-o", "--output_csv", default="centroid_distance.csv", help="Output CSV file name")
    parser.add_argument("-f", "--output_plot", default="centroid_distance.png", help="Output Plot image name")
    
    args = parser.parse_args()
    
    try:
        compute_centroid_distance(
            args.topology, args.trajectory, args.ligand, args.pocket, args.output_csv, args.output_plot
        )
    except Exception as e:
        print(f"\nError: {e}")
