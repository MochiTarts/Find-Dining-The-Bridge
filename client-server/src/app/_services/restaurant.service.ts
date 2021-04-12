import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, ReplaySubject } from 'rxjs';
import { environment } from '../../environments/environment';

const AUTH_API = '/api';
const OWNER_ENDPOINT = AUTH_API + '/owner';
const RO_ENDPOINT = AUTH_API + '/restaurant';
const DISH_ENDPOINT = AUTH_API + '/dish';
const UPLOAD_ENDPOINT = AUTH_API + '/cloud_storage/upload/';
const REMOVE_ENDPOINT = AUTH_API + '/cloud_storage/remove/';

@Injectable({
  providedIn: 'root'
})
export class RestaurantService {

  constructor(private http: HttpClient) {}

  /*
  @Input: restaurant id
  @Output: Google analytics data of restaurant page views
  */
  getViewTraffic(id:string): Observable<any> {
    const endpoint = RO_ENDPOINT + id + '/restaurant_traffic/'
    return this.http.get(endpoint)
  }

  /*
  @Input: None
  @Output: List of all approved restaurants

  Retrieves all restaurants that are approved
  */
  listRestaurants(): Observable<any> {
    const endpoint = RO_ENDPOINT + '/all/';
    return this.http.get(endpoint);
  }

  /*
  @Input: Restaurant id
  @Output: Corresponding restaurant object

  Retrieved the approved restaurant record provided the restaurant_id (can be obtained from the site url's query string)
  */
  getApprovedRestaurant(id:string): Observable<any> {
    const endpoint = RO_ENDPOINT + '/approved/' + id + '/';
    return this.http.get(endpoint);
  }

  /*
  @Input: None
  @Output: Corresponding restaurant object from pending collection

  Retrieved the pending restaurant record
  */
  getPendingRestaurant(): Observable<any> {
    const endpoint = RO_ENDPOINT + '/pending/';
    return this.http.get(endpoint);
  }

  /*
  @Input: JSON object containing restaurant owner info
          Required fields:
            user_id (number),
            restaurant_id (string)
  @Output: RO record

  Inserts a new restaurant_owner record into restaurant owner collection
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

  /*
  @Input: JSON object containing restaurant info
          Required fields:
            name (string),
            address (string),
            postalCode (string),
            owner_first_name (array),
            owner_last_name (array)
  @Output: JSON object of restaurant

  Updates an existing restaurant record in pending restaurant collection, marks the status to 'In_Progress'
  */
  updateRestaurantDraft(restInfo): Observable<any> {
    const endpoint = RO_ENDPOINT + '/draft/';
    return this.http.put<any>(endpoint, restInfo);
  }

  /*
  @Input: JSON object containing restaurant info
          Required fields:
            name (string),
            years (number),
            address (string),
            postalCode (string),
            phone (number),
            pricepoint (string),
            offer_options (array),
            bio (string),
            owner_first_name (array),
            owner_last_name (array),
            open_hours (string),
            payment_methods (array)
  @Output: JSON object of restaurant

  Inserts or update a new restaurant record into pending restaurant collection, marks the status to 'Pending'
  */
  insertRestaurantApproval(restInfo): Observable<any> {
    const endpoint = RO_ENDPOINT + '/submit/';
    return this.http.put<any>(endpoint, restInfo);
  }

  /*
  @Input: None
  @Output: JSON object containing:
            Dishes (a list of dish objects)

  Retrieves all pending dishes of a restaurant.
  */
  getPendingRestaurantFood(): Observable<any> {
    const endpoint = DISH_ENDPOINT + '/pending/';
    return this.http.get(endpoint);
  }

  /*
  @Input: restaurant id
  @Output: JSON object containing:
            Dishes (a list of dish objects)

  Retrieves all approved dishes of a restaurant using restaurant id (path parameter).
  */
  getApprovedRestaurantFood(restaurantId): Observable<any> {
    const endpoint = DISH_ENDPOINT + '/approved/' + restaurantId + '/';
    return this.http.get(endpoint);
  }

  /*
  @Input: None
  @Output: JSON object containing:
            Dishes (a list of dish objects)

  Retrieves all approved dishes from the database
  */
  getDishes(): Observable<any> {
    const endpoint = DISH_ENDPOINT + '/all/';
    return this.http.get(endpoint);
  }

  /*
  @Input: JSON object containing:
            name (string),
            description (string),
            price (string or number),
            specials (string),
            category (string)
  @Output: JSON object of dish record

  Inserts a new pending dish record
  */
  createPendingDish(dishInfo): Observable<any> {
    const endpoint = DISH_ENDPOINT + '/pending/';
    return this.http.post<any>(endpoint, dishInfo);
  }

  /*
  @Input: Dish info and dish id
          Nothing in the request body is required. But these are the only fields the request body can accept:
            JSON object containing:
              name (string),
              description (string),
              picture (string),
              price (string or number),
              specials (string),
              category (string)
  @Output: Updated JSON object of dish record

  Updates an existing dish record, provided the dish's id (path parameter)
  */
  editPendingDish(dishInfo, dishId): Observable<any> {
    const endpoint = DISH_ENDPOINT + '/pending/' + dishId + '/';
    return this.http.put<any>(endpoint, dishInfo);
  }

  /*
  @Input: JSON object containing:
            name (string),
            category (string)
  @Output: None

  Deletes the pending dish and approved dish from the database, given the dish name and the dish category
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
