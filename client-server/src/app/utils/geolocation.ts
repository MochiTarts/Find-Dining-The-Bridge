export class geolocation {
    
    static EARTH_RADIUS_METERS:number = 6371000;

    static haversineDistance(lat1, long1, lat2, long2){
        let theta_1 = geolocation.toRad(lat1);
        let theta_2 = geolocation.toRad(lat2);
        let delta_theta = geolocation.toRad(lat2 - lat1);
        let delta_lambda = geolocation.toRad(long2 - long1);
        // sin(D_lambda/2)^2 + cos(theta1) * cos(theta2) * sin(D_lambda/2)^2 = (1/2*chord length)^2
        let a = Math.pow(Math.sin(delta_theta/2),2) + Math.cos(theta_1) * Math.cos(theta_2) * Math.pow(Math.sin(delta_lambda/2), 2);
        // 2* atan2(sqrt(a), sqrt(1-a)) = the angular distance in radians 
        let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        // radius in meters * angular distance in radians = actual distance in meters
        let d = geolocation.EARTH_RADIUS_METERS * c;
        return d;
    }

    static toRad(degrees: number){
        return degrees * Math.PI / 180;
    }

}