# X-Booker User documentation

> This document is for the users to navigate and understand the X-Booker platform.

## Inviting teammates/organization members

Admins can invite other users to their organizations by visiting the organization/members page. They will be required to provide the new teammate's email and choose a role. An email will be sent to the invited user which will expire after 3 days. The invited user must log in within 3 days using the link specified in their email.
Before the admins can invite a teammate to their organization they have to purchase a license for the new teammate. They need to purchase licenses for every one of their teammates including them. To put it simply, if an organization has an admin and 4 teammates with different roles assigned to them then they need to purchase 5 licenses. At the end of the month if the admin chooses not to renew their subscription plans or if for any reason the payment did not go through then the organization will be unusable from the user's end. But all the automation will keep working till the organization is completely blocked from the x-booker system.

## Subscription plans

X-Booker has different types of subscription plans that enables different capabilities for the organizations. Such organization storage & member count. Navigate to the Organization > Billing to see the current plans and make modifications to your billing info.

## Setting up the organization

Organizations need a bit of configuration to perform as they expected. The first and most important part of an organization is the Google account. Usually, the user who created the organization is responsible for updating the organization's Google account. But the admins can also change the organization's root Google account. This setting is found on the organization's profile page. Along with other important settings.
The admins then need to upload their pricing list to the organization. This list has to be a CSV file that has an x-booker pricing schema. The default currency for x-booker is £ GBP (Pound sterling). So if the price list is in other currencies then the system will not interpret the prices correctly. Admins can also download a sample price list and update the files with their prices and products. To get the sample file click on the "i" button in the top right corner of the price list section and then click the download sample file button. For now, JSON, ODF, or any other files are not supported as the price list. Each of the products in the price list can also have multiple extras/sub-products.
Express delivery marker
When editing the price list the user can specify a sub-product for express delivery by adding the "Express" word in the primary product name or the sub-product name. This express keyword will tell the system to mark the product as an express delivery product this affects the survey report release date and the deadline for Field Agents.
Valuation marker
If the user wants to mark their product for a valuation request they can add the "valuation" word to the name of the product or in the sub-product and the system will mark the product for valuation. For now, the valuation does not affect the survey report delivery time but will highlight the valuation request in the instructions.

## Automated emails

X Booker has 5 types of automated emails
- A survey report email that is automatically sent to the requested client
- A Booking date notifier email is sent to the client to inform them about the booking date for their booking requests
- Phone consultation email that is automatically sent to the client to inform them about the phone call date
- UCN email that is automatically sent to the client to inform them about the UCN for the x-booker. UCNs are unique client ids in the x-booker system
- Invitation email that is used only when sending a teammate invitation
- Admins can edit these emails to their needs. These emails also have variables that the users can use to get information from the system. Such as client emails, booking dates, organization names, etc.

## Simple email client

There is a built-in email client in the x-booker. Users can use the email client to quickly send, read, and reply emails. This is not on par with Google’s Gmail but is capable of quick email management so that the users don’t have to keep switching their browser tabs or applications. The email client supports the latest HTML, JS, and CSS along with attachments and links. It has issues with supporting older emails though. Especially if the emails are targeted to the desktop sites then the

## Client booking requests

Clients can send booking requests to the organization from the forms page of the organization. All the organizations have a unique client-side form from where clients can submit booking requests. To get the organization's form link visit the organization page and click on the clipboard icon beside the "Booking Form Link" text. The form link is structured in this way http://x-booker.app/forms/bookings/{{ organization_id }}.

Clients will enter information about themselves, the property, and their agents and submit the request to the organization. As they submit the request the system will create a new client profile if not already present then will send a notification email with the UCN. This event will also create a new task on the default To-Do list in the Kanban board. If the organization has an active booking team then the task will mention all the booking team members (since we don't have a metrics system that will assign tasks based on the pending jobs).
The booking team can then confirm the booking request by assigning a Field Agent to it. They can perform this from the single booking request view page. Right after a Field agent is assigned to a booking request an email notification will be sent to the requested client and will create a new task that will mention the assigned field agent.

Booking team members and the admins can modify the booking dates and the client submitted information at any point. But making changes after the survey report is sent will not update the survey report nor the booking date. But it is possible to send the survey report multiple times and also set the booking dates as many times as needed. Admins can also update the kanbans and tasks when needed. From the single booking view page admins and booking team members can quickly send emails to the client if they have to. There is also a file uploading option to better organize the requests. Field agents, the booking team, and admins can upload files related to the booking request for future use.

The Field agents will get their assigned jobs on the jobs panel. There they can upload the survey report for the booking team's approval. The booking team will verify the survey report and send it to the client. The admins can also upload survey reports, verify them, and then send them to the client. The admins can perform all the tasks the other team members can.

If needed, the booking team can duplicate/create a new booking request from the existing booking request with all the client and property information init or modify parts of it and assign a new field agent to the newly created booking request (instruction).

## X-Booker Dashboard Guide

### Default Page/Dashboard

The default landing page is the dashboard page, where users can find information about their organization. They have the option to toggle the quick info card from their profile page. Quick access cards for tasks, bookings, and recent messages are available. Users can also hide certain info graphs if desired.

On the tasks quick view panel, users can click the plus button to visit the all tasks/kanban page. Within the quick view panel, users can switch task statuses and remove tasks.

The bookings and messages quick view panel offer similar functionalities.

### Contacts Page

The contacts page lists both the organization's clients and members. Admins can remove clients by clicking the "i" button, which expands the client's information. Admins can also send emails to clients by clicking the email button or call them directly by clicking the caller button (the call opens on their mobile device, not in the browser).

Admins can invite new clients to the organization by clicking the "Add contact" button, which takes them to a new page with a form. By filling out the form, they can send a quick booking form link to potential clients.

In the member view, admins cannot remove members directly, but clicking on the cards will take them to the member's profile page, where they can remove a member.

### Calendar Page

The calendar page allows members and admins to view the associated Google calendar and create/modify events. All automated events also appear here. The calendar offers three viewing options: month, week, and day view. Clicking on the rectangular boxes opens a new event modal, allowing users to create new events by filling out the form and confirming. These events are synced with their Google calendar, enabling users to view them there as well. Updating event details from Google calendar or removing them will also remove the event from X-Booker.

Admins can choose to view events from all departments or toggle to view events from a single department only.

By default, the organization does not have any calendars, so admins need to manually add their calendar IDs or choose to auto-create all the required calendars.

### Profile Page

The profile page serves as the user's profile and preferences page. Users can upload a new profile picture, change their names, and update contact details. However, they cannot change their primary email/Google account because doing so would require creating a new X-Booker profile.


### Messages Page

The messages page features the built-in messaging system of X-Booker. Organization members can use this system to interact with each other instead of relying on external communication mediums. Messages are real-time and send notifications to the user on the other side. Users can share images and PDFs in the chat. However, messages do not support external links, bold, or italic texts.

If a user cannot locate the person they want to connect with, they can click the "New" button to start a conversation with them.

There is a default organization conversation group where users can send messages visible to all other members of the organization.

### Emails Page

The built-in email client on X-Booker is simple and easy to use. It is not as robust as Gmail and lacks advanced features such as spam filters, junk folders, and auto-sorting. The email client allows sorting emails by labels and supports nested labels, similar to Gmail. It is built with the latest versions of HTML, CSS, and JavaScript. However, older emails may not display correctly due to styling limitations. If an email does not display correctly, users can click on the "Text Version" at the bottom of the email viewer to access the plain text version. Users can also perform actions on emails, such as marking them as spam or important, removing them, or starring them. The email client can display attachments unless they are

 in an unknown format for the browser.

Users can send emails with attachments by clicking the "Compose" button.

### Kanban Page

The Kanban page serves as a task management system for the organization. Admins can create new Kanban groups for specific teams. For example, if admins want a "To-Do" group dedicated to the booking team, they can create a new Kanban group and select the booking department. This Kanban group will be visible only to the booking team and admins. If a department has permission to view Kanban groups, they can modify or create new tasks within the groups and mention teammates.

### Organization Page

The organization button on the side panel provides access to several sub-pages. The profile button takes the user to the organization's profile page, where admins can change the organization's logo, address, contact email, and contact number. Admins can also remove the current Google account and add a new one if necessary.

In the price list section, admins can update the organization's price list. They can also download a sample price list by clicking the "i" button in the top-right corner of the price list section. Next to the price list, there is a "Manage Subscription" button, which takes the user to the organization's plans page. Clicking "Manage Plans" redirects admins to the Stripe customer portal, where they can upgrade or remove subscription plans.

In the organization's departments section, there is an "All Members" button that allows admins to manage members. They can add or remove members from the organization or departments from this page. Note that admins cannot remove themselves if there are no other admins in the organization.

In the automated emails section, admins can modify email designs. The emails include system variables such as client name, client email, and organization's email. Using these variables in emails will automatically replace them with the appropriate information. For example, "#CLIENT_NAME#" will be replaced by the name of the client the email is sent to.

In the bottom-left corner of the organization's page, there are buttons to add members and access the organization's files. Clicking "Show Organization's Files" takes admins to the built-in file manager, which supports folders and files. However, nesting folders within folders is not supported. All reports sent to users and uploaded files within the organization appear in the file manager (reports are under the "Reports" folder).

The integrations page under the organization's section contains integrations and X-Booker webhook settings, which are currently under development.

### Bookings Page

The bookings page displays a list of all bookings and instructions made by the organization. This page is accessible only to administrators and the booking team. Users can filter bookings based on their status and have the option to archive or mark a booking as deleted. Switching to the "Deleted Bookings" view allows users to see all bookings marked as deleted, with the ability to restore or completely remove them from the system by pruning. Users can also export all their booking data as CSV and other file formats (work in progress).

Clicking on a booking takes users to the single booking view page, where admins and the booking team can manage and interact with bookings. In the bottom-right corner, a three-dot button expands and shows quick action buttons. The first button displays activities related to the booking/instruction, such as creation and report submission dates. The next button, "Duplicate Booking," allows admins or the booking team to create a new booking/instruction by copying information from the current booking request. They can then assign a new field agent to the booking.

The page also features a file upload feature, enabling the team to upload files relevant to the booking request. Files can be downloaded or viewed in browsers, and file links can be attached to the booking.

The edit button allows admins or

 the booking team to modify the booking, except for removing uploaded files. They can also remove the assigned field agent or mark the instruction as deleted.

### Invoices Page

Invoices are automatically generated for bookings. Invoices can include QR codes but are not generated automatically. The invoices page offers two viewing modes: "Resolved" and "Unhandled." The "Resolved" mode displays invoices that have been paid by clients.

### Jobs Page

The jobs page lists all jobs assigned to a field agent. This page is primarily for field agents but can be viewed by admins as well (without job visibility). Field agents can sort and view their assigned jobs, upload reports or required files, and request the booking team's review. The team reviews the reports and sends them to clients.

### Reports Deposit

This is the section where field agents upload their reports and mark instructions/bookings for review.
