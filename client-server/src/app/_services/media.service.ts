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

  /**
   * Uploads image(s) and/or a video for a given PendingRestaurant
   *
   * @param formData - FormData containing media info
   *                    media_type: value from media_type param
   *                    save_location: value from save_location param
   *                    media_file: FILE (attach your image file(s) or video file here)
   *                    image_captions: a stringified list of string
   *                    media_link: string (YouTube url)
   *                      - Use media_file if you're going to send a file to upload; leave media_link blank
   *                      - Use media_link if you're going to send a YouTube link; leave media_file blank
   *                    submit_for_approval: value from submit_for_approval
   * @param media_type - string (value must be either 'IMAGE' or 'VIDEO')
   * @param save_location - string (value must be 'cover_photo_url', 'logo_url', 'restaurant_image_url', or 'restaurant_video_url')
   * @param submit_for_approval - string (value must be 'True' or 'False'; NO LOWERCASE)
   *                                  - This tells backend if restaurant is saving draft or submitting it for admin approval
   *                                  True - submitting for admin approval
   *                                  False - saving as draft
   * @returns JSON object of the updated restaurant record
   */
  uploadRestaurantMedia(formData, media_type: string, save_location: string, submit_for_approval: string): Observable<any> {
    const endpoint = RO_MEDIA_ENDPOINT;
    formData.append('media_type', media_type);
    formData.append('save_location', save_location);
    formData.append('submit_for_approval', submit_for_approval);
    return this.http.put<any>(endpoint, formData);
  }

  /**
   * Deletes image(s) for a PendingRestaurant (associated with restaurant_image_url field)
   *
   * @param formData - FormData containing media info
   *                    restaurant_images: array of string (Array of image urls to remove)
   * @returns JSON object of the updated restaurant record
   */
  deleteRestaurantMedia(formData): Observable<any> {
    const endpoint = RO_MEDIA_ENDPOINT;
    const options = {
      headers: new HttpHeaders({}),
      body: formData,
    };
    return this.http.delete<any>(endpoint, options);
  }

  /**
   * Uploads dish image
   *
   * @param formData - FormData containing media info
   *                    media_type: string ('IMAGE' only)
   *                    media_file: FILE (the image file to be uploaded)
   *                    save_location: string ('picture' only)
   * @param dishId the updated Dish record
   * @returns
   */
  uploadDishMedia(formData, dishId): Observable<any> {
    const endpoint = DISH_MEDIA_ENDPOINT + dishId + '/';
    formData.append('media_type', 'IMAGE');
    formData.append('save_location', 'picture');
    return this.http.put<any>(endpoint, formData);
  }
}
