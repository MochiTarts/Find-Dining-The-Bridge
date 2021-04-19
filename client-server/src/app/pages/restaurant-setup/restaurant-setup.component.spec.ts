import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RestaurantSetupComponent } from './restaurant-setup.component';

describe('RestaurantSetupComponent', () => {
  let component: RestaurantSetupComponent;
  let fixture: ComponentFixture<RestaurantSetupComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RestaurantSetupComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RestaurantSetupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
