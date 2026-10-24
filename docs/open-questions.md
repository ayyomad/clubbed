# Open questions

When a question is resolved, move it to `decisions.md` as a decision and delete it here.

## Clubs and permissions
1. Can one club admin remove another admin, including the chairman?
2. A club must never drop to zero admins. How is this enforced?
3. Student club leadership changes yearly. How does the platform admin reassign admins?
4. How does an admin add a teammate: lookup by email, by register ID, or an invite?
5. Is "platform admin" Django's `is_superuser`, or a separate flag?

## Accounts
6. How is college email verified (link or OTP), and is the account inactive until verified?
7. Is the college email domain enforced at sign-up?

## Events and registration
8. Can club admins publish events freely, or does something approve them?
9. Can registration continue after the deadline? Who can close it early?
10. What happens to existing registrations when an event is cancelled?
11. Capacity: what stops two people from taking the last spot at the same moment?
12. Waitlist: in the MVP, or later?

## Teams
13. Is a user limited to one team per event?
14. Teams lock when registration closes, and a team below the minimum size is invalid. Confirm both.
15. Can the leader leave a team, or must they disband it or transfer leadership?

## Known issues with `diagrams/ER1.png`
- Remove the direct Event to FormAnswer line (an answer already reaches its event through its field and its registration).
- Check the Event/Team labels: one event has many teams.
- Add labels on the Club/ClubMembership line (one club, many memberships).
- Add the missing Team fields: event, leader (User), join code.
- `Registration` and `Team` both point to an event, so a validation rule is needed: the registration's event must equal its team's event. The same applies to `FormAnswer` and `FormField`.
- Check-in has no place in the diagram yet (`checked_in_at` on `Registration`).