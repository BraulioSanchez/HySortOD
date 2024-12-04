import common.AUC;
import common.Relation;
import common.search.TreeStrategy;
import net.sourceforge.argparse4j.ArgumentParsers;
import net.sourceforge.argparse4j.inf.ArgumentParser;
import net.sourceforge.argparse4j.inf.Namespace;
import outlier.HySortOD;

import java.util.Locale;

public class Main {

    static {
        Locale.setDefault(Locale.US);
    }

    static String input;
    static String inputSeparator;
    static int labelColumn;
    static boolean hasHeader;
    static int b;
    static int minSplit;
    static boolean reportOutput;

    public static void main(String[] args) {
        Namespace opts = processArguments(args);

        // read parameters
        input = opts.get("input");
        inputSeparator = opts.get("inputSeparator");
        labelColumn = opts.getInt("labelColumn");
        hasHeader = opts.getBoolean("hasHeader");
        b = opts.getInt("b");
        minSplit = opts.getInt("minSplit");
        reportOutput = opts.getBoolean("reportOutput");

        // read dataset
        Relation relation = Relation.readCSV(input, ",", labelColumn, true);

        int k = 10;
        double score = 0.;
        double runtime = 0.;
        double s = 0.05;
        for (int i = 0; i < k; i++) {
            Relation sample = relation.sample(s);

            long start, end;
            double[] yPred;
            int[] yTrue = sample.getLabels();

            // run the algorithm and compute runtime
            start = System.currentTimeMillis();
            HySortOD hsod = new HySortOD(b, new TreeStrategy(minSplit));
            yPred = hsod.score(sample);
            end = System.currentTimeMillis();
            runtime += end - start;

            score += AUC.measure(yTrue, yPred);

            // report the outlierness score for each instance if specified
            if (reportOutput) {
                if (relation.hasLabel()) {
                    for (int $i = 0; $i < yTrue.length; $i++) {
                        System.out.printf("%d,%.4f%n", yTrue[$i], yPred[$i]);
                    }
                } else {
                    for (double pred : yPred) {
                        System.out.printf("%.4f%n", pred);
                    }
                }
            }
        }
        System.out.printf("runtime %.4f%n", runtime / k);

        // calculate the auc score if possible
        if (relation.hasLabel()) {
            System.out.printf("auroc %.4f%n", score / k);
        }
    }

    public static Namespace processArguments(String[] args){
        ArgumentParser parser = ArgumentParsers.newFor("HySortOD").build().defaultHelp(true);
        parser.addArgument("--input").type(String.class).help("input file").required(true);
        parser.addArgument("--inputSeparator").type(String.class).help("separator in input file").setDefault(String.valueOf(","));
        parser.addArgument("--hasHeader").type(Boolean.class).help("input file has header").setDefault(Boolean.TRUE);
        parser.addArgument("--labelColumn").type(Integer.class).help("column of label (zero-based)").setDefault(0);
        parser.addArgument("--b").type(Integer.class).help("number of bins, must be greater than 1").setDefault(5);
        parser.addArgument("--minSplit").type(Integer.class).help("must be greater than 0").setDefault(100);
        parser.addArgument("--reportOutput").type(Boolean.class).help("report output").setDefault(Boolean.FALSE);
        return parser.parseArgsOrFail(args);
    }

}