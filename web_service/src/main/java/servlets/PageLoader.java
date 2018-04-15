package servlets;

import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;

/**		This class is used for loading and writing HTML pages	*/
public class PageLoader {
	
	//Send requested HTML page
	public void sendPage(PrintWriter writer, String path) throws IOException {
		String page = new String(Files.readAllBytes(Paths.get(path)));
		writer.write(page);
	}
	
	//Send HTML page with message
	public void sendPage(PrintWriter writer, String path, String message) throws IOException {
		String page = new String(Files.readAllBytes(Paths.get(path)));
		String[] parts = page.split("<body>");
		page = parts[0] + "<body><h2>" + message + "</h2>" + parts[1];
		writer.write(page);
	}
	
	//Send HTML page with Predicted Document Type
	public void sendPrediction(PrintWriter writer, String path, String prediction) throws IOException {
		String page = "<html><head>PREDICTION</head> <body></body></html>";
		String[] parts = page.split("<body>");
		page = parts[0] + "<body><h4>Result : " + prediction + "</h4>" + parts[1];
		writer.write(page);
	}
	
	//Send HTML page with Prediction and Confidence
	public void sendPrediction(PrintWriter writer, String path, String prediction, String confidence) 
			throws IOException {
		
		if(confidence.length() > 4) {
			confidence = confidence.substring(0, 5);
		}
		
		String page = "<html><head><h3>RESULT</h3></head> <body></body></html>";
		String[] parts = page.split("<body>");
		page = parts[0] + "<body><b>Prediction : " + prediction + "<br>Confidence : " + confidence +
				"</b>" + parts[1];
		writer.write(page);
	}
}
