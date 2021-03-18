import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RestaurantNearbyCardComponent } from './restaurant-nearby-card.component';

describe('RestaurantNearbyCardComponent', () => {
  let component: RestaurantNearbyCardComponent;
  let fixture: ComponentFixture<RestaurantNearbyCardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RestaurantNearbyCardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RestaurantNearbyCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
