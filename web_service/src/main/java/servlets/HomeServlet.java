package servlets;

import java.io.IOException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.nio.file.Files;
import java.nio.file.Paths;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.StringEntity;

import javax.servlet.ServletContext;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**		Main Servlet Class which loads the Home Page 
 * 		hosted on AWS Beanstalk
 */
public class HomeServlet extends HttpServlet{
	
	private static final long serialVersionUID = 6148214731003375966L;
	
	
	/**		URL to AWS Lambda endpoint	*/
	private final String LAMBDA_URL = "https://x41c47q7c7.execute-api.us-east-1.amazonaws.com/dev";
	private final String HOMEPAGE_PATH = "WEB-INF/classes/html/loginPage.html";
	

	@Override
	public void doGet(HttpServletRequest request, HttpServletResponse response){
		
		ServletContext context = getServletContext();
		String context_path = request.getServletPath();
		PageLoader pageLoader = new PageLoader();
		
		/**		Home Page	*/
		System.out.println("Home page");
		if(context_path.matches("/")) {
			try {
				response.setContentType("text/html");
				PrintWriter writer = response.getWriter();
				
				String path = getServletContext().getRealPath(HOMEPAGE_PATH);
				pageLoader.sendPage(writer, path);
				context.log("Response : HomePage");
				
			} catch (IOException e) {
				context.log("IOException : Could not find HomePage");
			}
		}
		
		
		
		/**		Request for predicting document type */
		
		else if(context_path.matches("/prediction")) {
			String url_encoded_words = request.getParameter("words");
			
			//If the URL did not contain "words" parameter
			if(url_encoded_words == null) {
				context.log("Exception : Did not receive \"words\" in query string");
				//return HomePage with dialogue
				try {
					response.setContentType("text/html");
					PrintWriter writer = response.getWriter();
					
					String path = getServletContext().getRealPath(HOMEPAGE_PATH);
					pageLoader.sendPage(writer, path, "Please Enter Words for prediction");
					context.log("Response :	HomePage with msg");
					
				} catch (IOException e) {
					context.log("IOException : Could not send redirect");
				}
				return;
			}
			
			
			//Decode the encoded url
			String words_string = new String();
			try {
				words_string = URLDecoder.decode(url_encoded_words, "UTF-8");
				
			} catch (UnsupportedEncodingException e) {
				context.log("UnsupportedEncodingException : Could not decode URL query string");
			}
			
			//Package the data into a json request
			JSONObject json = new JSONObject();
			String[] words = new String[]{words_string};
			try {
				json.put("data", words);
				
			} catch (JSONException e) {
				context.log("JSON ParseException");
			}
			
			
			//Call the API for predictions on these words
			JSONObject jsonResponseObj = new JSONObject();
			try {
				CloseableHttpClient client = HttpClients.createDefault();
			    HttpPost httpPost = new HttpPost(LAMBDA_URL);
			    httpPost.setEntity(new StringEntity(json.toString(), ContentType.APPLICATION_JSON));
				
			    httpPost.addHeader("Accept", "application/json");
			    httpPost.addHeader("Content-type", "application/json");
			    
			    CloseableHttpResponse httpResponse = client.execute(httpPost);
			    
				int statusCode = httpResponse.getStatusLine().getStatusCode();
				context.log("Status Code from Lambda : " + statusCode);
				String jsonResponseString = EntityUtils.toString(httpResponse.getEntity());
				
				jsonResponseObj = new JSONObject(jsonResponseString);
								
			} catch(Exception e) {
				context.log("Exception in sending Post request of json body to AWS Lambda");
				try {
					pageLoader.sendPage(response.getWriter(), HOMEPAGE_PATH, "Error sending Request");
					return;
				} catch (IOException e1) {
				}
			}
			
			//Display the predictions on HomePage
			try {
				JSONArray predictionArray = jsonResponseObj.getJSONArray("prediction");
				JSONArray confidenceArray = jsonResponseObj.getJSONArray("confidence");
				String prediction = predictionArray.getString(0);
				String confidence = confidenceArray.getString(0);
				
				response.setContentType("text/html");
				PrintWriter writer = response.getWriter();
				
				String path = getServletContext().getRealPath(HOMEPAGE_PATH);
				pageLoader.sendPrediction(writer, path, prediction, confidence);
				context.log("Response :	Prediction page");
				
			} catch (Exception e) {
				context.log("Exception : Display Prediction on HomePage");
				try {
					pageLoader.sendPage(response.getWriter(), HOMEPAGE_PATH,
							"Error. Kindly make sure the model is loaded");
					return;
				} catch (IOException e1) {
				}
			}
		}
	}
	
	
	@Override
	public void doPost(HttpServletRequest request, HttpServletResponse response) {
		try {
			response.sendRedirect("/");
			
		} catch (IOException e) {
			getServletContext().log("Exception : Redirecting from POST");
		}
	}
}
