package common;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.stream.Stream;

import org.apache.commons.lang3.StringUtils;

public class Relation implements Cloneable {

	private String name;
	private final int numRows;
	private final int numCols;
	private final Instance[] instances;
	private boolean hasLabel;
	private boolean isNormalized;
	private boolean[] datatypes; // true: continuous, false: categorical

	public Relation(int numRows, int numCols, Instance[] instances, String name, boolean hasLabel) {
		this.name = name;
		this.numRows = numRows;
		this.numCols = numCols;
		this.instances = instances;
		this.hasLabel = hasLabel;
		this.isNormalized = false;
	}

	public Relation(int numRows, int numCols, Instance[] instances, String name, boolean hasLabel, boolean[] datatypes) {
		this.name = name;
		this.numRows = numRows;
		this.numCols = numCols;
		this.instances = instances;
		this.hasLabel = hasLabel;
		this.isNormalized = false;
		this.datatypes = datatypes;
	}

	public static Relation readCSV(String filename) {
		return readCSV(filename, ",");
	}

	public static Relation readCSV(String filename, String sep) {
		return readCSV(filename, sep, -1, false);
	}

	public static Relation readCSV(String filename, String sep, int labelCol, boolean hasHeader) {
		int nRows = getNumRows(filename) - 1;
		int nCols = getNumCols(filename, sep);
		int nDataCols = nCols;
		boolean hasLabel = false;
		boolean[] datatypes = null;

		if (hasHeader) {
			nRows -= 1;
		}

		if (labelCol >= 0) {
			hasLabel = true;
			nDataCols -= 1;
		}

		Instance[] instances = new Instance[nRows];

		try (BufferedReader bf = new BufferedReader(new FileReader(filename))) {
			String line;
			String[] v;
			int label = -1;

			if (hasHeader) { // skip header
				bf.readLine();
			}

			line = bf.readLine(); // read data types
			v = line.split(sep);
			datatypes = new boolean[hasLabel ? v.length - 1 : v.length];
			for (int i = 0; i < datatypes.length; i++) {
				if ("con".equalsIgnoreCase(v[i])) {
					datatypes[i] = true;
				} else if ("cat".equalsIgnoreCase(v[i])) {
					datatypes[i] = false;
				}
			}

			for (int i = 0; (line = bf.readLine()) != null; i++) {
				v = line.split(sep);
				double[] values = new double[nDataCols];

				for (int j = 0; j < v.length; j++) {
					if (hasLabel && j == labelCol) {
						label = (int) Double.parseDouble(v[j]);
					} else {
						values[j] = Double.parseDouble(v[j]);
					}
				}

				instances[i] = new Instance(i, values, label);
			}
		} catch (IOException e) {
			e.printStackTrace();
		}

		return new Relation(nRows, nDataCols, instances, getName(filename), hasLabel, datatypes);
	}

	public Relation sampling(final int sampleSize) {
		ArrayList<Integer> ids = new ArrayList<Integer>(getNumRows());
		for (int i = 0; i < getNumRows(); i++) {
			ids.add(i);
		}

		Collections.shuffle(ids);

		Instance[] instances = new Instance[sampleSize];
		for (int i = 0; i < sampleSize; i++) {
			instances[i] = getInstance(ids.get(i));
		}

		return new Relation(sampleSize, getNumCols(), instances, "", hasLabel());
	}

	public Relation sampling(final int sampleSize, final Random rnd) {
		ArrayList<Integer> ids = new ArrayList<Integer>(getNumRows());
		for (int i = 0; i < getNumRows(); i++) {
			ids.add(i);
		}

		Collections.shuffle(ids, rnd);

		Instance[] instances = new Instance[sampleSize];
		for (int i = 0; i < sampleSize; i++) {
			instances[i] = getInstance(ids.get(i));
		}

		return new Relation(sampleSize, getNumCols(), instances, "", hasLabel(), getDatatypes());
	}

	public double[][] computeMinMax() {
		int dimensions = this.numCols;
		double[] mins = new double[dimensions], maxs = new double[dimensions];
		for (int d = 0; d < dimensions; d++) {
			mins[d] = Double.MAX_VALUE;
			maxs[d] = -Double.MAX_VALUE;
		}

		for (int i = 0; i < this.numRows; i++) {
			for (int d = 0; d < dimensions; d++) {
				final double v = this.getAt(i, d);
				mins[d] = (v < mins[d]) ? v : mins[d];
				maxs[d] = (v > maxs[d]) ? v : maxs[d];
			}
		}
		return new double[][] { mins, maxs };
	}

	private static String getName(String filename) {
		String basename = Paths.get(filename).getFileName().toString();
		return basename.substring(0, basename.lastIndexOf("."));
	}

	private static int getNumCols(String filename, String sep) {
		try {
			Stream<String> stream = Files.lines(Paths.get(filename));
			String header = stream.iterator().next();
			stream.close();
			return (int) StringUtils.countMatches(header, sep) + 1;
		} catch (IOException e) {
			return 0;
		}
	}

	private static int getNumRows(String filename) {
		try {
			Path path = Paths.get(filename);
			return (int) Files.lines(path).count();
		} catch (IOException e) {
			return 0;
		}
	}

	public boolean isNormalized() {
		return isNormalized;
	}

	public Instance getInstance(int i) {
		return instances[i];
	}

	public double getAt(int i, int j) {
		return instances[i].getAt(j);
	}

	public void setAt(int i, int j, double value) {
		instances[i].setAt(j, value);
	}

	public List<Instance> asList() {
		return Arrays.asList(this.instances);
	}

	public Instance[] getInstances() {
		return instances;
	}

	public int[] getLabels() {
		int[] labels = new int[numRows];
		for (int i = 0; i < numRows; i++) {
			labels[i] = getInstance(i).getLabel();
		}
		return labels;
	}

	public int getNumRows() {
		return numRows;
	}

	public int getNumCols() {
		return numCols;
	}

	public String getName() {
		return name;
	}

	public boolean hasLabel() {
		return hasLabel;
	}

	public boolean[] getDatatypes() {
		return datatypes;
	}

	@Override
	public Relation clone() {
		int id, lbl;
		double[] vals;
		Instance[] instances = new Instance[numRows];

		for (int i = 0; i < numRows; i++) {
			id = this.instances[i].getId();
			vals = this.instances[i].getValues();
			lbl = this.instances[i].getLabel();
			instances[i] = new Instance(id, vals, lbl);
		}
                
                boolean[] datatypes = new boolean[numCols];
                for (int j = 0; j < numCols; j++)
                        datatypes[j] = getDatatypes()[j];

		return new Relation(numRows, numCols, instances, new String(name), hasLabel, datatypes);
	}
        
        public Relation sample(double s) {
		int id = 0, lbl;
		double[] vals;
		ArrayList<Instance> instances = new ArrayList();
		
                int numOut = 0;
                for (int i = 0; i < numRows; i++)
                    if (this.instances[i].getLabel() == 1)
                        numOut++;
                double p = (s * (numRows - numOut) / (1 - s)) / numOut;
                
		for (int i = 0; i < numRows; i++) {
                        lbl = this.instances[i].getLabel();
                        if (lbl == 0 || Math.random() < p) {
                            vals = this.instances[i].getValues();
                            instances.add(new Instance(id++, vals, lbl));
                        }
		}
                
                boolean[] datatypes = new boolean[numCols];
                for (int j = 0; j < numCols; j++)
                        datatypes[j] = getDatatypes()[j];
                
                return new Relation(id, numCols, instances.toArray(new Instance[0]), new String(name), hasLabel, datatypes);
	}        
}
