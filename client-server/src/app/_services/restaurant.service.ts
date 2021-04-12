import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

const AUTH_API = '/api';
const OWNER_ENDPOINT = AUTH_API + '/owner';
const RO_ENDPOINT = AUTH_API + '/restaurant';
const DISH_ENDPOINT = AUTH_API + '/dish';

@Injectable({
  providedIn: 'root'
})
export class RestaurantService {

  constructor(private http: HttpClient) {}

  /**
   * Retrieves all restaurants that are approved
   * @returns List of all approved restaurants
   */
  listRestaurants(): Observable<any> {
    const endpoint = RO_ENDPOINT + '/all/';
    return this.http.get(endpoint);
  }

  /**
   * Retrieved the approved restaurant record provided the restaurant_id (can be obtained from the site url's query string)
   * @param id - Restaurant id
   * @returns Corresponding restaurant object
   */
  getApprovedRestaurant(id:string): Observable<any> {
    const endpoint = RO_ENDPOINT + '/approved/' + id + '/';
    return this.http.get(endpoint);
  }

  /**
   * Retrieved the pending restaurant record
   * @returns Corresponding restaurant object from pending collection
   */
  getPendingRestaurant(): Observable<any> {
    const endpoint = RO_ENDPOINT + '/pending/';
    return this.http.get(endpoint);
  }

  /**
   * Inserts a new restaurant_owner record into restaurant owner collection
   * 
   * @param ownerInfo - JSON object containing restaurant owner info
   *                      Required fields:
   *                        user_id (number),
   *                        restaurant_id (string)
   * @returns RO record
   */
  roSignup(ownerInfo): Observable<any> {
    const endpoint = OWNER_ENDPOINT + '/signup/';
    return this.http.post<any>(endpoint, ownerInfo);
  }

  /**
   * Updates a restaurant_owner record in the database
   * 
   * @param ownerInfo - JSON object containing:
   *                      consent_status (string)
   * @returns Updated RO record in JSON format
   */
  roEdit(ownerInfo): Observable<any> {
    const endpoint = OWNER_ENDPOINT + '/profile/';
    return this.http.put<any>(endpoint, ownerInfo);
  }

  /*
  @Input: JSON object containing restaurant info
          Required fields:
            name, address, postalCode, email, owner_first_name, owner_last_name (all are strings)
  @Output: JSON object of restaurant

  Inserts a new restaurant record into pending restaurant collection, status is marked as 'In_Progress'
  */
  insertRestaurantDraft(restInfo): Observable<any> {
    const endpoint = RO_ENDPOINT + '/draft/';
    return this.http.post<any>(endpoint, restInfo);
  }

  /**
   * Updates an existing restaurant record in pending restaurant collection,
   * marks the status to 'In_Progress'
   * 
   * @param restInfo - JSON object containing restaurant info
   *                   Required fields:
   *                     name (string),
   *                     address (string),
   *                     postalCode (string),
   *                     owner_first_name (array),
   *                     owner_last_name (array)
   * @returns JSON object of restaurant
   */
  updateRestaurantDraft(restInfo): Observable<any> {
    const endpoint = RO_ENDPOINT + '/draft/';
    return this.http.put<any>(endpoint, restInfo);
  }

  /**
   * Inserts or update a new restaurant record into pending restaurant collection,
   * marks the status to 'Pending'
   * 
   * @param restInfo - JSON object containing restaurant info
   *                   Required fields:
   *                     name (string),
   *                     years (number),
   *                     address (string),
   *                     postalCode (string),
   *                     phone (number),
   *                     pricepoint (string),
   *                     offer_options (array),
   *                     bio (string),
   *                     owner_first_name (array),
   *                     owner_last_name (array),
   *                     open_hours (string),
   *                     payment_methods (array)
   * @returns JSON object of restaurant
   */
  insertRestaurantApproval(restInfo): Observable<any> {
    const endpoint = RO_ENDPOINT + '/submit/';
    return this.http.put<any>(endpoint, restInfo);
  }

  /**
   * Retrieves all pending dishes of a restaurant.
   * @returns JSON object containing:
   *           Dishes (a list of dish objects)
   */
  getPendingRestaurantFood(): Observable<any> {
    const endpoint = DISH_ENDPOINT + '/pending/';
    return this.http.get(endpoint);
  }

  /**
   * Retrieves all approved dishes of a restaurant
   * using restaurant id (path parameter).
   * 
   * @param restaurantId - restaurant id
   * @returns JSON object containing:
   *           Dishes (a list of dish objects)
   */
  getApprovedRestaurantFood(restaurantId): Observable<any> {
    const endpoint = DISH_ENDPOINT + '/approved/' + restaurantId + '/';
    return this.http.get(endpoint);
  }

  /**
   * Retrieves all approved dishes from the database
   * @returns JSON object containing:
   *           Dishes (a list of dish objects)
   */
  getDishes(): Observable<any> {
    const endpoint = DISH_ENDPOINT + '/all/';
    return this.http.get(endpoint);
  }

  /**
   * Inserts a new pending dish record
   * 
   * @param dishInfo - JSON object containing:
   *                     name (string),
   *                     description (string),
   *                     price (string or number),
   *                     specials (string),
   *                     category (string)
   * @returns JSON object of dish record
   */
  createPendingDish(dishInfo): Observable<any> {
    const endpoint = DISH_ENDPOINT + '/pending/';
    return this.http.post<any>(endpoint, dishInfo);
  }

  /**
   * Updates an existing dish record, provided the dish's id (path parameter)
   * 
   * @param dishInfo - Nothing in the request body is required. But these are the only fields the request body can accept:
   *                   JSON object containing:
   *                     name (string),
   *                     description (string),
   *                     picture (string),
   *                     price (string or number),
   *                     specials (string),
   *                     category (string)
   * @param dishId - dish id
   * @returns 
   */
  editPendingDish(dishInfo, dishId): Observable<any> {
    const endpoint = DISH_ENDPOINT + '/pending/' + dishId + '/';
    return this.http.put<any>(endpoint, dishInfo);
  }

  /**
   * Deletes the pending dish and approved dish from the database, given the dish name and the dish category
   * @param dishInfo - JSON object containing:
   *                     name (string),
   *                     category (string)
   */
  deleteDish(dishInfo): void {
    const endpoint = DISH_ENDPOINT + '/pending/';
    const options = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
      }),
      body: dishInfo,
    };
    this.http.delete<any>(endpoint, options).subscribe((data) => {});
  }

}
