# Issue debugging and monitoring guide

In order to debug issues happening in production, you need to get as much information as
possible on the issue. It helps reproducing or directly fixing the issue. In addition,
you want to monitor it to see how it evolves or if it is fixed for good.

The tools used at SWH to get insights on issue happening in production are Sentry and
Kibana.

## Sentry overview

SWH instance URL: <https://sentry.softwareheritage.org/>

The service requires a login password pair to access, but does not require the SWH VPN
access. To sign up, click "Request to join" and provide your SWH developer email address
for the admins to create the account.

Official documentation: <https://docs.sentry.io/product/>

Sentry is specifically geared towards debugging production issues. In the "Issues" pane,
it presents issues grouped by similarity with statistics about their occurrence. Issues
can be filtered by:
- project (i.e. SWH service repository), e.g. "swh-loader-core" or "swh-vault";
- environment, e.g. "production" or "staging";
- time range.

Viewing a particular issue, you can access:

- the execution trace at the point of error, with pretty-printed local variables at each
  stack frame, as you would get in a post-mortem debugging session;
- contextual metadata about the running environment, which includes:
    - the first and last occurrence as detected by Sentry,
    - corresponding component versions,
    - installed packages,
    - entrypoint parameters,
    - runtime environment such as the interpreter version, the hostname¸ or the logging
      configuration.
- the breadcrumbs view, which shows several event log lines produced in the same run
  prior to the error. These are not the logs produced by the application, but events
  gathered through Sentry integrations.

## Debugging SWH services with Sentry

Here we show a specific type of issue that is characteristic of microservice
architectures as implemented at SWH. One difficulty may arise in finding where an issue
originates, because the execution is split between multiple services. It results in a
chain of linked issues, potentially one for each service involved.

Errors of type `RemoteException` encapsulate an error occurring in the service called
through a RPC mechanism. If the information encapsulated in this top-level error is not
sufficient, one would search for complementary traces by filtering the "Issues" view by
the linked service's project name.

Example:

Sentry issue: <https://sentry.softwareheritage.org/organizations/swh/issues/5026/?project=11>

The error appear as `<RemoteException 500 HttpResponseError: ['Download stream interrupted.']>`
A request from a vault cooker to the storage service had a network error.

Thanks to Sentry we see also which was the specific storage requested:

    `<RemoteStorage url=http://storage01.euwest.azure.internal.softwareheritage.org:5002/>`

Upon searching in the storage service issues, we find a corresponding `HttpResponseError`:
<https://sentry.softwareheritage.org/organizations/swh/issues/3857/?project=3>

We skip through the error reporting logic in the trace to get to the operation that was
performed. We see that this error comes in turn from a RPC call to the objstorage service:

    HttpResponseError: "Download stream interrupted." at `swh/storage/objstorage.py` in `content_get` at line 41

This is a transient network error: it should not persist when retrying. So a solution
might be to add a retrying mechanism somewhere in this chain of RPC calls.

## Issue monitoring with Sentry

Aggregated error traces as shown in the "Issues" pane are the primary source of
information for monitoring. This includes the statistics of occurrence for a given
period of time.

Sentry also comes with issue management features, that notably let you silence or
resolve errors. Silencing means the issue will still be recorded but not notified.
Resolving means the issue will be hidden from the default view, and any new occurrence
of it will specifically notify the issue owner that the issue still arises and is in
fact not resolved. Make sure an owner is associated to the issue, typically through
ownership rules set in the project settings.

For more info on monitoring issues, refer to:
<https://docs.sentry.io/product/error-monitoring/>

## Kibana overview

SWH instance URL: <http://kibana0.internal.softwareheritage.org:5601/app/kibana/>
Access to the SWH VPN is needed, but credentials are not.

Related wiki page: <https://intranet.softwareheritage.org/wiki/Kibana>

Official documentation: <https://www.elastic.co/guide/en/kibana/current/index.html>

Kibana is a visualization UI for searching through indexed logs. You can search through
different sources of logs in the "Discover" pane. The sources configured include
application logs for SWH services and system logs. You can also access dashboards shared
by other on a particular topic or create our own from a saved search.

There are 2 query languages which are quite similar: Lucene or KQL. Whatever one you
choose, you will have the same querying capabilities. A query tries to match values for
specific keys, and support many predicates and combination of them. See the
documentation for KQL: https://www.elastic.co/guide/en/kibana/current/kuery-query.html

To get logs for a particular service, you have to know the name of its systemd unit and
the hostname of the production server providing this service. For a worker, switch the
index pattern to "swh_workers-*", for another SWH service switch it to "systemlogs-*".

Example for getting swh-vault production logs:

With the index pattern set to "systemlogs-*", enter the KQL query:

    `systemd_unit:"gunicorn-swh-vault.service" AND hostname:"vangogh"`

Upon expanding a log entry with the leading arrow icon, you can inspect the entry in a
structured way. You can filter on particular values or fields, using the icons that are
left to the desired field. Fields including "message", "hostname" or "systemd_unit" are
often the most informational. You can also view the entry in context, several entries
before and after chronologically.

## Issue monitoring with Kibana

You can use Kibana saved searches and dashboards to follow issues based on associated
logs. Of course, we need to have logs produced that are related to the issue we want to
track.

You can save a search, as opposed to only a query, to easily get back to it or include
it in a dashboard. Just click "Save" in the top toolbar above the search bar. It
includes the query, filters, selected columns, sorting and index pattern.

Now you may want to have a customizable view of these logs, along with graphical
presentations. In the "Dashboard" pane, create a new dashboard. Click "add" in the top
toolbar and select your saved search. It will appear in resizable panel. Now doing a
search will restrict the search to the dataset configured for the panels.

To create more complete visualizations including graphs, refer to:
<https://www.elastic.co/guide/en/kibana/current/dashboard.html>
