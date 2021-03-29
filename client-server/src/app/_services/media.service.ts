import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

const AUTH_API = '/api';
const RO_MEDIA_ENDPOINT = AUTH_API + '/restaurant/media/';
const DISH_MEDIA_ENDPOINT = AUTH_API + '/dish/media/';

@Injectable({
  providedIn: 'root'
})
export class MediaService {

  constructor(private http: HttpClient) { }

  /*
  @Input: FormData containing media info
            media_type: string (IMAGE or VIDEO)
            save_location: string (cover_photo_url, logo_url, restaurant_image_url, restaurant_video_url)
            media_file: FILE (attach your image file(s) or video file here)
            media_link: string (YouTube url)
              - Use media_file if you're going to send me a file to upload; leave media_link blank
              - Use media_link if you're going to send me a YouTube link; leave media_file blank
            first_time_submission: string (True or False; NO LOWERCASE)
              - This tells backend if request is coming from the initial restaurant setup form, or it's coming from the editing restaurant profile page area
              True - coming from initial setup form
              False - coming from restaurant profile editing page
  @Output: Restaurant record

  Uploads images and videos for a given PendingRestaurant
  */
  uploadRestaurantMedia(formData, media_type: string, save_location: string, first_time_submission: string): Observable<any> {
    const endpoint = RO_MEDIA_ENDPOINT;
    formData.append('media_type', media_type);
    formData.append('save_location', save_location);
    formData.append('first_time_submission', first_time_submission);
    return this.http.put<any>(endpoint, formData);
  }

  /*
  @Input: FormData containing media info
            restaurant_images: array of string (Array of image urls to remove)
  @Output: Restaurant record

  Delets image(s) for a PendingRestaurant (associated with restaurant_image_url)
  */
  deleteRestaurantMedia(formData): Observable<any> {
    const endpoint = RO_MEDIA_ENDPOINT;
    const options = {
      headers: new HttpHeaders({}),
      body: formData,
    };
    return this.http.delete<any>(endpoint, options);
  }

  /*
  @Input: FormData containing media info
            media_type: string (IMAGE only)
            media_file: FILE (the image file to be uploaded)
            save_location: string (picture only)
  @Output: Dish record

  Uploads dish image
  */
  uploadDishMedia(formData, dishId): Observable<any> {
    const endpoint = DISH_MEDIA_ENDPOINT + dishId + '/';
    formData.append('media_type', 'IMAGE');
    formData.append('save_location', 'picture');
    return this.http.put<any>(endpoint, formData);
  }
}
