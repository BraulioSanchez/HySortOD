package common.search;

import java.util.HashMap;
import java.util.Objects;

public class Node {
	
	// Index information
	public final int value, begin, end;
	public final HashMap<Integer, Node> children;
	
	public Node(int value, int begin, int end) {
		children = new HashMap<>();
		this.value = value;
		this.begin = begin;
		this.end = end;
	}
	
	@Override
	public String toString() {
		return "(" + value + "," + begin + "," + end + ")";
	}

	public void add(Node node) {
		if (Objects.nonNull(node)) {
			children.put(node.value, node);
		}
	}

}