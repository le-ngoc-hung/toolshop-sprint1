Feature: Shopping cart
  As a shopper
  I want to add products with a chosen quantity
  So that I can verify the cart totals before checkout

  Background:
    Given I am on the home page

  Scenario Outline: Adding a product calculates the cart totals
    When I open the product "<product>"
    And I add it to the cart with quantity <quantity>
    And I open the cart
    Then the cart contains product "<product>"
    And the line price equals the unit price times quantity
    And the cart total equals the sum of the line prices

    Examples:
      | product            | quantity |
      | Combination Pliers  | 1        |
      | Claw Hammer         | 3        |
