import java.util.Locale;

import common.AUC;
import common.Relation;
import net.sourceforge.argparse4j.ArgumentParsers;
import net.sourceforge.argparse4j.inf.ArgumentParser;
import net.sourceforge.argparse4j.inf.Namespace;

public class Main {

	static {
        Locale.setDefault(Locale.US);
    }

    static String input;
	static int labelColumn;
	static double alpha;

	public static void main(String[] args) {
		ArgumentParser parser = ArgumentParsers.newFor("Analyze - HDoutliers result").build().defaultHelp(true);
        parser.addArgument("--input").type(String.class).help("dataset results").required(true);
		parser.addArgument("--labelColumn").type(Integer.class).help("column of label (zero-based)").setDefault(0);
		Namespace opts = parser.parseArgsOrFail(args);

		input = opts.get("input");
		labelColumn = opts.getInt("labelColumn");

		final Relation dataset = Relation.readCSV(input, ",", labelColumn, true);
		final double[] yPred = new double[dataset.getNumRows()];
		final int[] yTrue = dataset.getLabels();

		Relation result = Relation.readCSV(
				"competitors/HDoutliers/results/output_" + dataset.getName() + ".txt", ",", -1, true);
		for (int i = 0; i < dataset.getNumRows(); i++)
			yPred[i] = result.getInstance(i).getAt(0);
		double score = AUC.measure(yTrue, yPred);
		System.out.printf("auroc %.4f%n", score);
	}
}
