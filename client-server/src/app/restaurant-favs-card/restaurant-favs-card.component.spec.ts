import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RestaurantFavsCardComponent } from './restaurant-favs-card.component';

describe('RestaurantFavsCardComponent', () => {
  let component: RestaurantFavsCardComponent;
  let fixture: ComponentFixture<RestaurantFavsCardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RestaurantFavsCardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RestaurantFavsCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
