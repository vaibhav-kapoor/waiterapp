import org.alexd.jsonrpc.*;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class WaiterappClient {
	/**
	 * @param args
	 * @throws JSONException 
	 */
	public static void main(String[] args) throws JSONException {
		// // Create client specifying JSON-RPC version 2.0
		JSONRPCClient service = JSONRPCClient.create(
                "http://TheLegace:web2py@www.bes.waiterapp.ca/waiterapp/default/call/jsonrpc",
                JSONRPCParams.Versions.VERSION_1);
		service.setConnectionTimeout(2000);
		service.setSoTimeout(2000);
		try 
		{  
			
			JSONArray count = (JSONArray) service.call(
                    "restaurants_area","43.7747943","-79.7420149","2");
			System.out.println(count);
			count = (JSONArray) service.call("restaurants_area");
			System.out.println(count);
			
			/*for(int i=0;i<count.length();i++){
				JSONObject r = count.getJSONObject(i);
				System.out.println(r.get("id"));
			}*/
			
			JSONObject restaurant = count.getJSONObject(0);
			int id = restaurant.getInt("id");
			
			JSONObject check = (JSONObject) service.call("check_in", id);
			System.out.println(check);
			
			JSONArray menu = (JSONArray) service.call("restaurant_menu");
			System.out.println(menu);
			
			JSONObject reserve = (JSONObject) service.call("reserve_table", 4);
			System.out.println(reserve);
			
			JSONObject orderItem = (JSONObject) service.call("order_item", 1, 4, true);
			System.out.println(orderItem);
			
			JSONArray orders = (JSONArray) service.call("order_poll");
			System.out.println(orders);
			
			
		}
		catch (JSONRPCException e)
		{
		  e.printStackTrace();
		}

	}

}
