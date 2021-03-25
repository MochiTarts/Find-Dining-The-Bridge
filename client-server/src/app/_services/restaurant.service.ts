import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, ReplaySubject } from 'rxjs';
import { environment } from '../../environments/environment';

const AUTH_API = '/api';
const OWNER_ENDPOINT = AUTH_API + '/owner';
const RO_ENDPOINT = AUTH_API + '/restaurant';
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
  @Output: List of all restaurants

  Return list of all restaurants in the database
  */
  listRestaurants(): Observable<any> {
    const endpoint = RO_ENDPOINT + '/all/';
    return this.http.get(endpoint);
  }

  /*
  @Input: Restaurant id
  @Output: Corresponding restaurant object

  Returns the details of the restaurant using its id.
  */
  getApprovedRestaurant(id:string): Observable<any> {
    const endpoint = RO_ENDPOINT + '/approved/' + id + '/';
    return this.http.get(endpoint);
  }

  /*
  @Input: Restaurant id
  @Output: Corresponding restaurant object from pending collection

  Returns the details of the restaurant using its id.
  */
  getPendingRestaurant(): Observable<any> {
    const endpoint = RO_ENDPOINT + '/pending/';
    return this.http.get(endpoint);
  }

  /*
  @Input: Restaurant id
  @Output: Corresponding restaurant object with dishes

  Returns the details of the restaurant dishes using its id.
  */
  getRestaurantFood(id:string): Observable<any> {
    const endpoint = RO_ENDPOINT + '/dish/' + id + '/';
    return this.http.get(endpoint);
  }

  /*
  @Input: Restaurant id
  @Output: Corresponding restaurant object with dishes

  Returns the details of the restaurant dishes using its id.
  */
  getPendingRestaurantFood(id:string): Observable<any> {
    const endpoint = RO_ENDPOINT + '/dish/get_pending_by_restaurant/';
    var params = {
      restaurant_id: id,
    };
    return this.http.get(endpoint, { params: params });
  }

  /*
  @Input: None
  @Output: All Dishes

  Returns All Dishes.
  */
  getDishes(): Observable<any> {
    const endpoint = RO_ENDPOINT + '/dish/';
    return this.http.get(endpoint);
  }

  // /*
  // @Input: JSON object containing restaurant info
  // @Output: The ID for that restaurant

  // Creates an entry for the restauant in the database and returns an id
  // */
  // getRestaurantID(restuarantInfo): Observable<any> {
  //   const endpoint = RO_ENDPOINT + '/draft/';
  //   const userToken = {
  //     idToken: restuarantInfo.idToken,
  //   };
  //   delete restuarantInfo.idToken;
  //   return this.http.post<any>(endpoint, restuarantInfo, { params: userToken });
  // }

  /*
  @Input: JSON object containing dish info
  @Output: None

  Creates an entry for the dish for a particular restuarant using its id.
  */
  createDish(dishInfo): Observable<any> {
    const endpoint = RO_ENDPOINT + '/dish/p/';
    return this.http.post<any>(endpoint, dishInfo);
  }

  /*
  @Input: JSON object containing dish info
  @Output: None

  Creates an entry for the dish for a particular restuarant using its id.
  */
  editDish(dishInfo): Observable<any> {
    const endpoint = RO_ENDPOINT + '/dish/p/';
    return this.http.put<any>(endpoint, dishInfo);
  }

  /*
  @Input: JSON object containing dish name and restaurant id
  @Output: None

  Delete dish using dish name and restaurant id.
  */
  deleteDish(dishInfo): void {
    const endpoint = RO_ENDPOINT + '/dish/' + dishInfo.restaurant_id + '/';
    this.http.post<any>(endpoint, dishInfo).subscribe((data) => {});
  }

  /*
  @Input: JSON object containing restaurant owner info
          Required: user_id (number), restaurant_id (string)
  @Output: RO record

  Return a RO record
  */
  roSignup(ownerInfo): Observable<any> {
    const endpoint = OWNER_ENDPOINT + '/signup/';
    return this.http.post<any>(endpoint, ownerInfo);
  }

  /*
  @Input: JSON object containing restaurant info
  @Output: None

  Insert new restaurant as a draft into database
  */
  insertRestaurantDraft(restInfo): Observable<any> {
    const endpoint = RO_ENDPOINT + '/draft/';
    return this.http.post<any>(endpoint, restInfo);
  }

  /*
  @Input: JSON object containing restaurant info
  @Output: None

  Updates an existing restaurant record in pending restaurant collection, marks the status to 'In_Progress'
  */
  updateRestaurantDraft(restInfo): Observable<any> {
    const endpoint = RO_ENDPOINT + '/draft/';
    return this.http.put<any>(endpoint, restInfo);
  }

  /*
  @Input: JSON object containing restaurant info
  @Output: None

  Inserts or update a new restaurant record into pending restaurant collection, marks the status to 'Pending'
  */
  insertRestaurantApproval(restInfo): Observable<any> {
    const endpoint = RO_ENDPOINT + '/submit/';
    return this.http.put<any>(endpoint, restInfo);
  }

  uploadRestaurantMedia(formData, id, location): Observable<any> {
    const endpoint = UPLOAD_ENDPOINT;

    if (location == 'cover') {
      formData.append('save_location', 'cover_photo_url');
    } else if (location == 'logo') {
      formData.append('save_location', 'logo_url');
    } else if (location == 'owner') {
      formData.append('save_location', 'owner_picture_url');
    } else if (location == 'video') {
      formData.append('save_location', 'restaurant_video_url');
    } else if (location == 'image') {
      formData.append('save_location', 'restaurant_image_url');
    }

    formData.append('app', 'restaurant_RestaurantMedia');
    formData.append('_id', id);

    return this.http.post<any>(endpoint, formData);
  }

  uploadFoodMedia(formData, id): Observable<any> {
    const endpoint = UPLOAD_ENDPOINT;

    formData.append('save_location', 'picture');
    formData.append('app', 'restaurant_FoodMedia');
    formData.append('_id', id);

    return this.http.post<any>(endpoint, formData);
  }

  removeRestaurantImage(formData, id, location): Observable<any> {
    const endpoint = REMOVE_ENDPOINT;
    if (location == 'image') {
      formData.append('save_location', 'restaurant_image_url');
    }

    formData.append('app', 'restaurant_RestaurantMedia');
    formData.append('_id', id);

    return this.http.post<any>(endpoint, formData);
  }
}
