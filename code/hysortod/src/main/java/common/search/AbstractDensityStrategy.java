package common.search;

import common.Hypercube;

abstract class AbstractDensityStrategy implements IDensityStrategy {

	// Max hypercube neighborhood density
	protected int maxDensity;
	
	// Local reference for search
	protected Hypercube[] H; 

        @Override
	public int getMaxDensity() {
		return maxDensity;
	}

	protected boolean isImmediate(Hypercube hi, Hypercube hk) {
		final int[] p = hi.getCoords();
		final int[] q = hk.getCoords();
		for (int j = p.length - 1; j >= 0; j--)
			if (Math.abs(p[j] - q[j]) > 1)
				return false;
		return true;
	}

}