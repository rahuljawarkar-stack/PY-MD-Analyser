# Py-MD Analyser (PocketOccupancy & Centroid Distance Tracker)

**Designed & Developed by Dr. Rahul D. Jawarkar**
Department of Pharmaceutical Chemistry, Dr. Rajendra Gode Institute of Pharmacy, Ghatkheda, University mardi road, Amravati, Maharashtra, India (444602).

## 1. Introduction & Scientific Rationale
Welcome to the Py-MD Analyser! This software is a universal professional Python GUI application designed specifically for computational chemists and biophysicists to rigorously evaluate the stability of any molecular dynamics (MD) complexes (e.g., protein-ligand, protein-protein, or protein-peptide interactions).

While traditional Ligand RMSD measures internal flexibility, this software computes the **Ligand-Centroid to Pocket-Centroid Distance**, providing a direct quantitative measure of the ligand's translational displacement from the active site binding pocket over time.

## 2. Features
- **Universal Topology/Trajectory Support**: Powered by MDTraj & MDAnalysis, it can analyze any valid topology (PDB, GRO, CMS) and trajectory (DTR, XTC, TRR) output.
- **Centroid Distance Calculation**: Computes geometric centroid distances between heavy atoms of the ligand and the binding pocket.
- **Protein-Ligand RMSD**: Computes and overlays both Protein Backbone RMSD and Ligand Heavy-Atom RMSD for structural stability analysis.
- **Dynamic Cross-Correlation Matrix (DCCM)**: Analyzes correlated atomic motions, featuring interactive Min/Max scale adjustments in the GUI.
- **Root Mean Square Fluctuation (RMSF)**: Maps atomic flexibility per residue across the simulation.
- **Radius of Gyration (Rg)**: Tracks the compactness of the protein over time.
- **Hydrogen Bonding**: Utilizes the Wernet-Nilsson algorithm to accurately track specific Protein-Ligand Hydrogen Bonds over time.
- **SASA (Solvent Accessible Surface Area)**: Calculates the exposed surface area of the protein to track folding stability via the Shrake-Rupley algorithm.
- **Auto-Padding Engine**: Seamlessly fixes atom mismatches caused by Desmond Maestro exporting (e.g., stripped pseudo-atoms) so trajectories load flawlessly.
- **Multithreaded GUI**: Built with PyQt6 and QThread to ensure the UI remains responsive even when processing trajectories with >100,000 frames.
- **Publication-Ready Plotting**: Generates high-contrast, zero-margin plots optimized for scientific journals directly in the UI.
- **Native PDF Export**: Instantly export a comprehensive User Manual directly from the GUI as a PDF.
- **Exporting**: Save raw analytical data directly to CSV/Excel, and export all plots as high-resolution PNGs.

## 3. Installation Requirements
Requires Python 3.10 or 3.11+.

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 4. Usage
Run the application using:
```bash
launch.bat
# or
python main.py
```

### 2. Procedure to Perform Analysis in Py-MD Analyser
Follow these exact steps to run your analysis successfully:
1. **Load Topology File:** Click the `Load Topology File` button and select your coordinate file (e.g., `.pdb`, `.cms`, or `.gro`). *Note: Py-MD Analyser will automatically handle Desmond Maestro pseudo-atom stripping issues!*
2. **Load Trajectory:** Click the `Load Trajectory (DTR)` button and select the folder containing your trajectory data (for Desmond, this is usually a folder ending in `_trj`).
3. **Input Ligand Selection:** In the text box, type the identifier for your ligand (e.g., `resname UNK` or `resSeq 900`).
4. **Input Pocket Selection:** In the text box, define the residues making up your binding pocket (e.g., `resid 10-20` or `resSeq 10 to 20`).
5. **Set Cutoff & Stride:** Set the Distance Cutoff (in Å) to define what counts as "Occupied". Set the Stride to 1 to analyze every single frame.
6. **Execute:** Click the green **Run Analysis** button. The Activity Log will track progress, and results will appear in the tabs on the right!

## 3. Justification for Cutoff Values
Unlike standard atomic interaction distances (which measure edge-to-edge contacts at ~2.5 - 3.5 Å), the **Centroid Distance** measures the bulk displacement between the center of mass of the ligand and the center of the pocket. Because ligands and pockets have volume, their centroids will never perfectly overlap (0.0 Å).
- **3.0 - 5.0 Å (Default):** Recommended for standard drug-like molecules. If the ligand centroid drifts more than 5.0 Å from the pocket centroid, it indicates the bulk of the molecule has left the primary binding cleft and diffused towards the solvent.
- **> 6.0 Å:** Only justified for very large, elongated binding pockets (like extended peptide binding grooves) where the ligand can slide significantly while remaining bounded.

## 4. Interpreting Results
- **Stable flat line (e.g., < 3 Å):** The ligand forms a highly stable interaction network and remains securely anchored throughout the simulation.
- **Initial jump followed by flat line:** Represents "Induced Fit" where the ligand relaxes from a suboptimal docked pose into a lower-energy conformation.
- **Continuous large fluctuations (> 5-10 Å):** Indicates low binding affinity, with the ligand diffusing out into the bulk solvent.

## 5. Output & Export Options
- Navigate to the **Export** tab to save your raw statistical data (Distance, RMSD, RMSF, Rg, H-Bonds, SASA, DCCM) to CSV or Excel.
- Export publication-ready, high-resolution plots for journals directly from the GUI.
- Use the numerical input boxes in the **DCCM Heatmap** tab to dynamically adjust the matrix color scale (vmin/vmax) to highlight subtle correlations!
