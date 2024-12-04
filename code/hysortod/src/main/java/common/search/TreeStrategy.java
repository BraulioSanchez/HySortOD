package common.search;

import java.util.Objects;
import common.Hypercube;

public class TreeStrategy extends AbstractDensityStrategy {
	
	private Node root;
	
	// Minimum number of rows to allow sub-mapping 
	private final int minSplit;
		
	public TreeStrategy() {
		this(100);
	}
	
	public TreeStrategy(int minSplit) {		
                assert minSplit > 0;
		// Set the minimum number of rows to allow sub-mapping
		// When the value is 1 this parameter has no effect
		this.minSplit = minSplit;
	}

	@Override
	public void buildIndex(Hypercube[] H) {
		this.H = H;
		maxDensity = 0;
		
		// The root node maps the whole dataset
		root = new Node(-1, 0, H.length - 1);
		
		// Start recursive mapping from the first dimension
		buildIndex(root, 0);
	}
	
	private void buildIndex(Node parent, int col) {

		// Stop sub-mapping when the parent node maps less than minSplit hypercubes
		if (parent.end - parent.begin < minSplit)
			return;
		
		// Get the first value from the given range (minRowIdx, maxRowIdx)
		int value = H[parent.begin].getCoordAt(col);

		// Initialise the next range
		int begin = parent.begin;
		int end;

		// map the values in the current range
		int i = parent.begin + 1;
		for (; i <= parent.end; i++) {
		
			// when the value changes the node is created
			if (H[i].getCoordAt(col) != value) {
				
				// mark the end of the current value 
				end = i - 1;
				
				// create node for 'value' in 'col'
				Node child = new Node(value, begin, end);				
				parent.add(child);
				
				// map child values in the next dimension
				buildIndex(child, col + 1);

				// start new range
				begin = i;

				// update value
				value = H[i].getCoordAt(col);
			}
		}

		// map last value
		end = i - 1;
		Node child = new Node(value, begin, end);
		parent.add(child);

		buildIndex(child, col + 1);
	}
	
	private int density(int i, Node parent, int col) {
		int density = 0;
			
		if (parent.children.isEmpty()) {
			for (int k = parent.begin; k <= parent.end; k++) {
				if (isImmediate(H[i], H[k])) {
					density += H[k].getDensity();
				}
			}
		} else {

			int lftVal = H[i].getCoordAt(col) - 1;
			int midVal = H[i].getCoordAt(col);
			int rgtVal = H[i].getCoordAt(col) + 1;
			
			Node lftNode = parent.children.get(lftVal);
			Node midNode = parent.children.get(midVal);
			Node rgtNode = parent.children.get(rgtVal);

			density = (Objects.nonNull(lftNode) ? density(i, lftNode, col + 1) : 0) //
			+ (Objects.nonNull(midNode) ? density(i, midNode, col + 1) : 0)//
			+ (Objects.nonNull(rgtNode) ? density(i, rgtNode, col + 1) : 0);
		}
		
		return density;
	}

	@Override
	public int[] getDensities() {
		int n = H.length;
		int[] densities = new int[n];

		for (int i = 0; i < n; i++) {
			densities[i] = density(i, root, 0);
			maxDensity = Math.max(densities[i], maxDensity);
		}

		return densities;
	}
	
}