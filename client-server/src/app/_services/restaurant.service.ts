import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, ReplaySubject } from 'rxjs';
import { environment } from '../../environments/environment';

const AUTH_API = '/api';

@Injectable({
  providedIn: 'root'
})
export class RestaurantService {
  private static readonly RO_ENDPOINT = AUTH_API + '/restaurant';
  private static readonly UPLOAD_ENDPOINT = AUTH_API + '/cloud_storage/upload/';
  private static readonly REMOVE_ENDPOINT = AUTH_API + '/cloud_storage/remove/';
  constructor(private http: HttpClient) {}

  /*
  @Input: restaurant id
  @Output: Google analytics data of restaurant page views
  */
  getViewTraffic(id): Observable<any> {
    const endpoint = `${RestaurantService.RO_ENDPOINT}/get_restaurant_traffic/`
    const params = {
      'restaurant_id': id
    }
    return this.http.get(endpoint, { params: params })
  }

  /*
  @Input: None
  @Output: List of all restaurants

  Return list of all restaurants in the database
  */
  listRestaurants(): Observable<any> {
    const endpoint = `${RestaurantService.RO_ENDPOINT}/get_all/`;
    return this.http.get(endpoint);
  }

  /*
  @Input: Restaurant id
  @Output: Corresponding restaurant object

  Returns the details of the restaurant using its id.
  */
  getRestaurant(id): Observable<any> {
    const endpoint = `${RestaurantService.RO_ENDPOINT}/get/`;
    var params = {
      _id: id,
    };
    return this.http.get(endpoint, { params: params });
  }

  /*
  @Input: Restaurant id
  @Output: Corresponding restaurant object from pending collection

  Returns the details of the restaurant using its id.
  */
  getPendingRestaurant(id): Observable<any> {
    const endpoint = `${RestaurantService.RO_ENDPOINT}/get_pending/`;
    var params = {
      _id: id,
    };
    return this.http.get(endpoint, { params: params });
  }

  /*
  @Input: Restaurant id
  @Output: Corresponding restaurant object with dishes

  Returns the details of the restaurant dishes using its id.
  */
  getRestaurantFood(id): Observable<any> {
    const endpoint = `${RestaurantService.RO_ENDPOINT}/dish/get_by_restaurant/`;
    var params = {
      restaurant_id: id,
    };
    return this.http.get(endpoint, { params: params });
  }

  /*
  @Input: Restaurant id
  @Output: Corresponding restaurant object with dishes

  Returns the details of the restaurant dishes using its id.
  */
  getPendingRestaurantFood(id): Observable<any> {
    const endpoint = `${RestaurantService.RO_ENDPOINT}/dish/get_pending_by_restaurant/`;
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
    const endpoint = `${RestaurantService.RO_ENDPOINT}/dish/get_all/`;
    return this.http.get(endpoint);
  }

  /*
  @Input: JSON object containing restaurant info
  @Output: The ID for that restaurant

  Creates an entry for the restauant in the database and returns an id
  */
  getRestaurantID(restuarantInfo): Observable<any> {
    const endpoint = `${RestaurantService.RO_ENDPOINT}/save/`;
    const userToken = {
      idToken: restuarantInfo.idToken,
    };
    delete restuarantInfo.idToken;
    return this.http.post<any>(endpoint, restuarantInfo, { params: userToken });
  }

  /*
  @Input: JSON object containing dish info
  @Output: None

  Creates an entry for the dish for a particular restuarant using its id.
  */
  createDish(dishInfo): Observable<any> {
    const endpoint = `${RestaurantService.RO_ENDPOINT}/dish/insert_pending/`;
    return this.http.post<any>(endpoint, dishInfo);
  }

  /*
  @Input: JSON object containing dish info
  @Output: None

  Creates an entry for the dish for a particular restuarant using its id.
  */
  editDish(dishInfo): Observable<any> {
    const endpoint = `${RestaurantService.RO_ENDPOINT}/dish/edit_pending/`;
    return this.http.post<any>(endpoint, dishInfo);
  }

  /*
  @Input: JSON object containing dish name and restaurant id
  @Output: None

  Delete dish using dish name and restaurant id.
  */
  deleteDish(dishInfo): void {
    const endpoint = `${RestaurantService.RO_ENDPOINT}/dish/delete/`;
    this.http.post<any>(endpoint, dishInfo).subscribe((data) => {});
  }

  /*
  @Input: JSON object containing restaurant info (must have ID)
  @Output: None

  Edits information for a restuarant using its id.
  */
  editRestaurant(restInfo): Observable<any> {
    const endpoint = `${RestaurantService.RO_ENDPOINT}/edit/`;
    const userToken = {
      idToken: restInfo.idToken,
    };
    delete restInfo.idToken;
    return this.http.post<any>(endpoint, restInfo, { params: userToken });
  }

  uploadRestaurantMedia(formData, id, location): Observable<any> {
    const endpoint = `${RestaurantService.UPLOAD_ENDPOINT}`;

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
    const endpoint = `${RestaurantService.UPLOAD_ENDPOINT}`;

    formData.append('save_location', 'picture');
    formData.append('app', 'restaurant_FoodMedia');
    formData.append('_id', id);

    return this.http.post<any>(endpoint, formData);
  }

  removeRestaurantImage(formData, id, location): Observable<any> {
    const endpoint = `${RestaurantService.REMOVE_ENDPOINT}`;
    if (location == 'image') {
      formData.append('save_location', 'restaurant_image_url');
    }

    formData.append('app', 'restaurant_RestaurantMedia');
    formData.append('_id', id);

    return this.http.post<any>(endpoint, formData);
  }
}