import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RestaurantProfileFormComponent } from './restaurant-profile-form.component';

describe('RestaurantProfileFormComponent', () => {
  let component: RestaurantProfileFormComponent;
  let fixture: ComponentFixture<RestaurantProfileFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RestaurantProfileFormComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RestaurantProfileFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
