package outlier;

import java.util.Objects;

import common.BinaryTree;
import common.Hypercube;
import common.Instance;
import common.Relation;
import common.search.IDensityStrategy;
import common.search.TreeStrategy;

public class HySortOD {
	
	// number of bins
	public final int b;
	
	// hypercube's length
	private final double l;
		
	// Default hypercube mapper 
	private final IDensityStrategy strategy;
	
	public HySortOD() {
		this(5, new TreeStrategy());
	}

	public HySortOD(int b) {
		this(b, new TreeStrategy());
	}

	public HySortOD(IDensityStrategy strategy) {
		this(5, strategy);
	}
	
	public HySortOD(int b, IDensityStrategy strategy) {
		this.b = b;
		l = 1 / (double) b;
		this.strategy = strategy;
	}

	public double[] score(Relation X) {

		int[] W;
		double[] O;
		Hypercube[] H;
		int m = X.getNumRows();
		
		X.normalize();
		
		H = getSortedHypercubes(X);
                strategy.buildIndex(H);
		W = strategy.getDensities();
		O = getOutliernessScore(H, W, m);

		return O;
	}
	
	private Hypercube[] getSortedHypercubes(Relation X) {
		int m = X.getNumRows();
		BinaryTree<Hypercube> sorted = new BinaryTree<>();

		for (int i = 0; i < m; i++) {
			Hypercube h = new Hypercube(X.getInstance(i).getValues(), l);
			Hypercube obj = sorted.get(h);
			
			if (Objects.isNull(obj)) {
				h.add(X.getInstance(i));
				sorted.add(h);
			} else
				obj.add(X.getInstance(i));
		}
		
		int n = sorted.size();
		Hypercube[] H = new Hypercube[n];
		
		int i = 0;
		for (Hypercube h : sorted)
			H[i++] = h;
		
		return H;
	}

	private double[] getOutliernessScore(Hypercube[] H, int[] W, int m) {
            double[] O = new double[m];
            double value;
		
            int i = 0;
            for (Hypercube h : H) {
                value = score(W[i++]);
                for (Instance x : h.getInstances())
                    O[x.getId()] = value;
            }
		
            return O;
	}

	private double score(int density) {
		return 1 - ((double) density / strategy.getMaxDensity());
	}
}