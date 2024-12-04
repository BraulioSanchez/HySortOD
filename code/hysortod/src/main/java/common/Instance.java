package common;

public class Instance {
	
    private int id;
    private int label;
    private double[] values;

    public Instance(int id, double[] values) {
        this(id, values, -1);
    }

    public Instance(int id, double[] values, int label) {
        assert values.length > 0;
        this.id = id;
        this.label = label;
        this.values = new double[values.length];
        for (int i = 0; i < values.length; i++)
            this.values[i] = values[i];
    }

    @Override
    public String toString() {
        StringBuilder str = new StringBuilder();
        str.append(String.format("(%s, ", this.id));
        for(int i = 0; i < values.length - 1; i++)
            str.append(String.format("%.3f ", values[i]));
        str.append(String.format("%.3f, %s)", values[values.length - 1], this.label));
        return str.toString();
    }

    public int getId() {
        return id;
    }

    public double[] getValues() {
        return values;
    }

    public double getAt(int j) {
        return values[j];
    }

    public void setAt(int j, double value) {
        values[j] = value;
    }

    public int getLabel() {
        return label;
    }

    public boolean hasLabel() {
        return label >= 0;
    }

    public int getNumDimensions() {
    	return values.length;
    }
    
    public double distCat(Instance other, boolean[] isCategorical, int[] numDistinctValues) {
        double value = 0;
        for (int j = 0; j < values.length; j++)
            if (isCategorical[j] && this.values[j] != other.values[j])
                value += 1 - 1 / Math.pow(numDistinctValues[j], 2); // probability-based contribution: none of the values is fixed
        return Math.sqrt(value);
    }
}