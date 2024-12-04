package common;

import org.apache.commons.lang3.StringUtils;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import java.util.Map.Entry;
import java.util.stream.Stream;

public class Relation implements Cloneable {

    private final String name;
    private final int numRows;
    private final int numCols;
    private final Instance[] instances;
    private final boolean hasLabel;
    private boolean isNormalized;
    private final boolean[] isColCategorical;
    private final Map<Double, Integer>[] mapsCatCols; // a map <value, frequency> per categorical column

    public Relation(int numRows, int numCols, Instance[] instances, String name, boolean hasLabel,
                    boolean[] isColCategorical, Map<Double, Integer>[] mapsCatCols) {
        this.name = name;
        this.numRows = numRows;
        this.numCols = numCols;
        this.instances = instances;
        this.hasLabel = hasLabel;
        this.isNormalized = false;
        this.isColCategorical = isColCategorical;
        this.mapsCatCols = mapsCatCols;
    }

    public static Relation readCSV(String filename, String sep, int labelCol, boolean hasHeader) {
        int nRows = getNumRows(filename);
        int nDataCols = getNumCols(filename, sep);
        boolean hasLabel = false;

        if (hasHeader) {
            nRows -= 2;
        }

        if (labelCol >= 0) {
            hasLabel = true;
            nDataCols -= 1;
        }

        boolean[] isColCategorical = new boolean[nDataCols];

        Instance[] instances = new Instance[nRows];

        try (BufferedReader bf = new BufferedReader(new FileReader(filename))) {
            String line;
            String[] v;
            int label = -1;

            if (hasHeader) {
                bf.readLine(); // skip column names
                v = bf.readLine().split(sep); // read column types
                for (int j = 0; j < nDataCols; j++) {
                    if ("cat".equals(v[j])) {
                        isColCategorical[j] = true;
                    }
                }
            }

            for (int i = 0; (line = bf.readLine()) != null; i++) {
                v = line.split(sep);
                double[] values = new double[nDataCols];

                for (int j = 0; j < v.length; j++) {
                    if (j == labelCol) {
                        label = Integer.parseInt(v[j]);
                    } else {
                        values[j] = Double.parseDouble(v[j]);
                    }
                }

                instances[i] = new Instance(i, values, label);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        @SuppressWarnings("unchecked")
        TreeMap<Double, Integer> mapsCatCols[] = new TreeMap[nDataCols];
        for (int j = 0; j < nDataCols; j++) {
            if (isColCategorical[j]) {
                mapsCatCols[j] = new TreeMap<>();
            }
        }

        return new Relation(nRows, nDataCols, instances, getName(filename), hasLabel, isColCategorical, mapsCatCols);
    }

    private static String getName(String filename) {
        String basename = Paths.get(filename).getFileName().toString();
        return basename.substring(0, basename.lastIndexOf("."));
    }

    private static int getNumCols(String filename, String sep) {
        try (Stream<String> stream = Files.lines(Paths.get(filename))) {
            String header = stream.iterator().next();
            return StringUtils.countMatches(header, sep) + 1;
        } catch (IOException e) {
            return 0;
        }
    }

    private static int getNumRows(String filename) {
        Path path = Paths.get(filename);
        try (Stream<String> stream = Files.lines(path)) {
            return (int) stream.count();
        } catch (IOException e) {
            return 0;
        }
    }

    public void normalize() {
        assert !isNormalized;
        assert numRows > 0;
        assert numCols > 0;
        assert Objects.nonNull(instances);

        for (int j = 0; j < numCols; j++) {
            if (!isColCategorical[j]) {
                double minVal = Double.POSITIVE_INFINITY;
                double maxVal = Double.NEGATIVE_INFINITY;
                for (int i = 0; i < numRows; i++) {
                    minVal = Math.min(instances[i].getAt(j), minVal);
                    maxVal = Math.max(instances[i].getAt(j), maxVal);
                }
                for (int i = 0; i < numRows; i++) {
                    double value = (instances[i].getAt(j) - minVal) / (maxVal - minVal);
                    instances[i].setAt(j, value);
                }
            }
        }

        processCatCols(); // convert categorical columns into continuous ones, and normalize them

        isNormalized = true;
    }

    private void countFrequencies() {
        for (int j = 0; j < numCols; j++) {
            if (isColCategorical[j]) {
                for (int i = 0; i < numRows; i++) {
                    if (!mapsCatCols[j].containsKey(instances[i].getAt(j))) {
                        mapsCatCols[j].put(instances[i].getAt(j), 1);
                    } else {
                        mapsCatCols[j].replace(instances[i].getAt(j), mapsCatCols[j].get(instances[i].getAt(j)) + 1);
                    }
                }
            }
        }
    }

    private int minimumDescriptionLength(int[] sortedFrequencies) {
        int cutPoint = -1;
        int preAverage, postAverage;
        int descriptionLength, minimumDescriptionLength = Integer.MAX_VALUE;
        for (int i = 0; i < sortedFrequencies.length; i++) {
            descriptionLength = 0;

            // calculate the average of both sets
            preAverage = 0;
            for (int j = 0; j < i; j++)
                preAverage += sortedFrequencies[j];
            if (i > 0) {
                preAverage /= i;
                descriptionLength += Math.log10(1 + preAverage) / Math.log10(2); // change the log base from 10 to 2
            }
            postAverage = 0;
            for (int j = i; j < sortedFrequencies.length; j++)
                postAverage += sortedFrequencies[j];
            postAverage /= (sortedFrequencies.length - i);
            descriptionLength += Math.log10(1 + postAverage) / Math.log10(2); // change the log base from 10 to 2

            // calculate the description length
            for (int j = 0; j < i; j++) {
                // change the log base from 10 to 2
                descriptionLength += Math.log10(1 + Math.abs(preAverage - sortedFrequencies[j])) / Math.log10(2);
            }
            for (int j = i; j < sortedFrequencies.length; j++) {
                // change the log base from 10 to 2
                descriptionLength += Math.log10(1 + Math.abs(postAverage - sortedFrequencies[j])) / Math.log10(2);
            }

            // verify if this is the best cut point
            if (descriptionLength < minimumDescriptionLength) {
                cutPoint = i;
                minimumDescriptionLength = descriptionLength;
            }
        }
        return cutPoint;
    }

    private void processCatCols() {
        // get metadata about the categorical columns
        countFrequencies();
        int numCatCols = 0;
        int[] numDistinctValues = new int[numCols];
        for (int j = 0; j < numCols; j++) {
            if (isColCategorical[j]) {
                numDistinctValues[j] = getNumDistinctValues(j);
                numCatCols++;
            }
        }

        // process pivots only if there are categorical columns
        if (numCatCols > 0) {
            if (numCatCols == 1) { // single categorical column
                // find pivots
                int j = 0;
                // identify the categorical column j
                for(;!isColCategorical[j];j++)
                    ;
                List<Entry<Double, Integer>> listFrequencies = new ArrayList<>(mapsCatCols[j].entrySet());
                // sort frequencies keeping track of the original order
                listFrequencies.sort(Entry.comparingByValue());
                int[] sortedFrequencies = new int[numDistinctValues[j]];
                for (int i = 0; i < numDistinctValues[j]; i++) {
                    sortedFrequencies[i] = listFrequencies.get(i).getValue();
                }
                // cut point for the MDL-based selection
                int cutPoint = minimumDescriptionLength(sortedFrequencies);
                if (cutPoint == 0) {
                    cutPoint = numDistinctValues[j];
                }

                // create pivots
                Instance[] pivots = new Instance[cutPoint];
                double[] values = new double[numCols];
                for (int k = 0; k < cutPoint; k++) {
                    values[j] = listFrequencies.get(k).getKey();
                    pivots[k] = new Instance(k, values, 0);
                }

                // update column
                for (int i = 0; i < numRows; i++) {
                    // compute and sum distances
                    double value = 0;
                    for (int k = 0; k < cutPoint; k++) {
                        value += instances[i].distCat(pivots[k], isColCategorical, numDistinctValues);
                    }
                    // set new value
                    instances[i].setAt(j, value);
                }
            } else { // two or more categorical columns
                // find pivots
                int[] IDpivots = new int[numCatCols];
                int random = (int) Math.floor(Math.random() * numRows);
                double dist, maxDist;
                // first pivot
                IDpivots[0] = 0;
                maxDist = instances[IDpivots[0]].distCat(instances[random], isColCategorical, numDistinctValues);
                for (int i = 1; i < numRows; i++) {
                    dist = instances[i].distCat(instances[random], isColCategorical, numDistinctValues);
                    if (dist > maxDist) {
                        maxDist = dist;
                        IDpivots[0] = i;
                    }
                }
                // second pivot
                IDpivots[1] = 0;
                maxDist = instances[IDpivots[1]].distCat(instances[IDpivots[0]], isColCategorical, numDistinctValues);
                for (int i = 1; i < numRows; i++) {
                    dist = instances[i].distCat(instances[IDpivots[0]], isColCategorical, numDistinctValues);
                    if (dist > maxDist) {
                        maxDist = dist;
                        IDpivots[1] = i;
                    }
                }
                // other pivots
                for (int nextPivot = 2; nextPivot < numCatCols; nextPivot++) {
                    double minError = Double.POSITIVE_INFINITY, error;
                    for (int i = 0; i < numRows; i++) {
                        error = 0;
                        int k = 0;
                        for (; k < nextPivot; k++) {
                            if (i == IDpivots[k]) {
                                break;
                            }
                            dist = instances[i].distCat(instances[IDpivots[k]], isColCategorical, numDistinctValues);
                            error += Math.abs(maxDist - dist);
                        }
                        if (k == nextPivot && error < minError) {
                            minError = error;
                            IDpivots[nextPivot] = i;
                        }
                    }
                }

                // copy pivots
                Instance[] pivots = new Instance[numCatCols];
                for (int k = 0; k < numCatCols; k++) {
                    pivots[k] = new Instance(instances[IDpivots[k]].getId(), instances[IDpivots[k]].getValues(),
                            instances[IDpivots[k]].getLabel());
                }

                // update columns
                double[] values = new double[numCatCols];
                for (int i = 0; i < numRows; i++) {
                    // compute distances
                    for (int k = 0; k < numCatCols; k++) {
                        values[k] = instances[i].distCat(pivots[k], isColCategorical, numDistinctValues);
                    }
                    // set new values
                    int j = -1;
                    for (int k = 0; k < numCatCols; k++) {
                        for (j++; !isColCategorical[j]; j++)
                            ;
                        instances[i].setAt(j, values[k]);
                    }
                }
            }

            // normalize updated column(s)
            for (int j = 0; j < numCols; j++) {
                if (isColCategorical[j]) {
                    double minVal = Double.POSITIVE_INFINITY;
                    double maxVal = Double.NEGATIVE_INFINITY;
                    for (int i = 0; i < numRows; i++) {
                        minVal = Math.min(instances[i].getAt(j), minVal);
                        maxVal = Math.max(instances[i].getAt(j), maxVal);
                    }
                    for (int i = 0; i < numRows; i++) {
                        double value = (instances[i].getAt(j) - minVal) / (maxVal - minVal);
                        instances[i].setAt(j, value);
                    }
                }
            }
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

    public List<Instance> asList() {
        return Arrays.asList(this.instances);
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

    public int getNumDistinctValues(int j) {
        assert Objects.nonNull(mapsCatCols[j]);
        return mapsCatCols[j].size();
    }

    public double[] getDistinctValues(int j) {
        assert Objects.nonNull(mapsCatCols[j]);
        return Stream.of(mapsCatCols[j].keySet().toArray(new Double[0])).mapToDouble(Double::doubleValue).toArray();
    }

    public int[] getFrequencies(int j) {
        assert Objects.nonNull(mapsCatCols[j]);
        return Stream.of(mapsCatCols[j].values().toArray(new Integer[0])).mapToInt(Integer::intValue).toArray();
    }

    public boolean[] getIsColCategorical() {
        return isColCategorical;
    }

    public boolean hasLabel() {
        return hasLabel;
    }

    @Override
    public Relation clone() {
        int id, lbl;
        double[] vals;
        Instance[] instances = new Instance[numRows];
        boolean[] isColCategorical = new boolean[numCols];
        @SuppressWarnings("unchecked")
        Map<Double, Integer>[] mapsCatCols = new TreeMap[numCols];

        for (int i = 0; i < numRows; i++) {
            id = this.instances[i].getId();
            vals = this.instances[i].getValues();
            lbl = this.instances[i].getLabel();
            instances[i] = new Instance(id, vals, lbl);
        }

        for (int j = 0; j < numCols; j++) {
            isColCategorical[j] = this.isColCategorical[j];
            if (isColCategorical[j]) {
                mapsCatCols[j] = new TreeMap<>(this.mapsCatCols[j]);
            }
        }

        return new Relation(numRows, numCols, instances, name, hasLabel, isColCategorical, mapsCatCols);
    }

    public Relation sample(final double s) {
        int id = 0, lbl;
        double[] vals;
        ArrayList<Instance> instances = new ArrayList<>();
        boolean[] isColCategorical = new boolean[numCols];
        @SuppressWarnings("unchecked")
        Map<Double, Integer>[] mapsCatCols = new TreeMap[numCols];

        int numOut = 0;
        for (int i = 0; i < numRows; i++) {
            if (this.instances[i].getLabel() == 1) {
                numOut++;
            }
        }
        double p = (s * (numRows - numOut) / (1 - s)) / numOut;

        for (int i = 0; i < numRows; i++) {
            lbl = this.instances[i].getLabel();
            if (lbl == 0 || Math.random() < p) {
                vals = this.instances[i].getValues();
                instances.add(new Instance(id++, vals, lbl));
            }
        }

        for (int j = 0; j < numCols; j++) {
            isColCategorical[j] = this.isColCategorical[j];
            if (isColCategorical[j]) {
                mapsCatCols[j] = new TreeMap<>(this.mapsCatCols[j]);
            }
        }

        return new Relation(id, numCols, instances.toArray(new Instance[0]), name, hasLabel, //
                isColCategorical, mapsCatCols);
    }
}