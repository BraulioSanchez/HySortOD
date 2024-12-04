package common.search;

import common.Hypercube;

public interface IDensityStrategy {
	public void buildIndex(Hypercube[] H);
	public int[] getDensities();
	public int getMaxDensity();
}