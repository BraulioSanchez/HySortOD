import common.AUC;
import common.Relation;
import common.search.TreeStrategy;
import net.sourceforge.argparse4j.inf.Namespace;
import outlier.HySortOD;

import java.util.Locale;

public class Benchmark {

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
        Namespace opts = Main.processArguments(args);

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
        double s = 0.05;
        double bestScore = 0;
        double runtimeBestScore = 0.;
        int bBestScore = 0;
        int numRowsSampleBestScore = 0;
        for (int b = 2; b <= 100; b++) {
            double score = 0.;
            double runtime = 0.;
            int numRowsSample = 0;
            for (int i = 0; i < k; i++) {
                Relation sample = relation.sample(s);
                numRowsSample += sample.getNumRows();

                long start, end;
                double[] yPred;
                int[] yTrue = sample.getLabels();

                start = System.currentTimeMillis();
                HySortOD hsod = new HySortOD(b, new TreeStrategy(minSplit));
                yPred = hsod.score(sample);
                end = System.currentTimeMillis();
                runtime += end - start;

                score += AUC.measure(yTrue, yPred);
            }
            runtime /= k;
            score /= k;
            numRowsSample /= k;

            if (score > bestScore) {
                bestScore = score;
                runtimeBestScore = runtime;
                bBestScore = b;
                numRowsSampleBestScore = numRowsSample;
            }
        }
        message(relation.getName(), numRowsSampleBestScore, bBestScore, bestScore, runtimeBestScore);
    }

    private static void message(String dataset, int numRows, int b, double score, double runtime) {
        System.out.println("Best-fixed:");
        System.out.printf("%-15s\tn=%d\tb=%d\tAUROC=%.4f\tRuntime=%.4f%n", dataset, numRows, b, score, runtime);
    }
}