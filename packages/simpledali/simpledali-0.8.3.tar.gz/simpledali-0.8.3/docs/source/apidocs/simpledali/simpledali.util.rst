:py:mod:`simpledali.util`
=========================

.. py:module:: simpledali.util

.. autodoc2-docstring:: simpledali.util
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`datetimeToHPTime <simpledali.util.datetimeToHPTime>`
     - .. autodoc2-docstring:: simpledali.util.datetimeToHPTime
          :summary:
   * - :py:obj:`hptimeToDatetime <simpledali.util.hptimeToDatetime>`
     - .. autodoc2-docstring:: simpledali.util.hptimeToDatetime
          :summary:
   * - :py:obj:`utcnowWithTz <simpledali.util.utcnowWithTz>`
     - .. autodoc2-docstring:: simpledali.util.utcnowWithTz
          :summary:
   * - :py:obj:`isowithz <simpledali.util.isowithz>`
     - .. autodoc2-docstring:: simpledali.util.isowithz
          :summary:
   * - :py:obj:`hptimeAsIso <simpledali.util.hptimeAsIso>`
     - .. autodoc2-docstring:: simpledali.util.hptimeAsIso
          :summary:
   * - :py:obj:`optional_date <simpledali.util.optional_date>`
     - .. autodoc2-docstring:: simpledali.util.optional_date
          :summary:
   * - :py:obj:`prettyPrintInfo <simpledali.util.prettyPrintInfo>`
     - .. autodoc2-docstring:: simpledali.util.prettyPrintInfo
          :summary:
   * - :py:obj:`encodeAuthToken <simpledali.util.encodeAuthToken>`
     - .. autodoc2-docstring:: simpledali.util.encodeAuthToken
          :summary:
   * - :py:obj:`decodeAuthToken <simpledali.util.decodeAuthToken>`
     - .. autodoc2-docstring:: simpledali.util.decodeAuthToken
          :summary:
   * - :py:obj:`timeUntilExpireToken <simpledali.util.timeUntilExpireToken>`
     - .. autodoc2-docstring:: simpledali.util.timeUntilExpireToken
          :summary:

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`MICROS <simpledali.util.MICROS>`
     - .. autodoc2-docstring:: simpledali.util.MICROS
          :summary:
   * - :py:obj:`INFO_VERSION <simpledali.util.INFO_VERSION>`
     - .. autodoc2-docstring:: simpledali.util.INFO_VERSION
          :summary:
   * - :py:obj:`INFO_SERVERID <simpledali.util.INFO_SERVERID>`
     - .. autodoc2-docstring:: simpledali.util.INFO_SERVERID
          :summary:
   * - :py:obj:`INFO_CAPABILITIES <simpledali.util.INFO_CAPABILITIES>`
     - .. autodoc2-docstring:: simpledali.util.INFO_CAPABILITIES
          :summary:
   * - :py:obj:`INFO_STATUS <simpledali.util.INFO_STATUS>`
     - .. autodoc2-docstring:: simpledali.util.INFO_STATUS
          :summary:
   * - :py:obj:`INFO_STREAMLIST <simpledali.util.INFO_STREAMLIST>`
     - .. autodoc2-docstring:: simpledali.util.INFO_STREAMLIST
          :summary:
   * - :py:obj:`INFO_STREAM <simpledali.util.INFO_STREAM>`
     - .. autodoc2-docstring:: simpledali.util.INFO_STREAM
          :summary:

API
~~~

.. py:data:: MICROS
   :canonical: simpledali.util.MICROS
   :value: 1000000

   .. autodoc2-docstring:: simpledali.util.MICROS

.. py:function:: datetimeToHPTime(time)
   :canonical: simpledali.util.datetimeToHPTime

   .. autodoc2-docstring:: simpledali.util.datetimeToHPTime

.. py:function:: hptimeToDatetime(hptime)
   :canonical: simpledali.util.hptimeToDatetime

   .. autodoc2-docstring:: simpledali.util.hptimeToDatetime

.. py:function:: utcnowWithTz()
   :canonical: simpledali.util.utcnowWithTz

   .. autodoc2-docstring:: simpledali.util.utcnowWithTz

.. py:function:: isowithz(dt)
   :canonical: simpledali.util.isowithz

   .. autodoc2-docstring:: simpledali.util.isowithz

.. py:function:: hptimeAsIso(hptime)
   :canonical: simpledali.util.hptimeAsIso

   .. autodoc2-docstring:: simpledali.util.hptimeAsIso

.. py:function:: optional_date(date_str)
   :canonical: simpledali.util.optional_date

   .. autodoc2-docstring:: simpledali.util.optional_date

.. py:data:: INFO_VERSION
   :canonical: simpledali.util.INFO_VERSION
   :value: 'Version'

   .. autodoc2-docstring:: simpledali.util.INFO_VERSION

.. py:data:: INFO_SERVERID
   :canonical: simpledali.util.INFO_SERVERID
   :value: 'ServerID'

   .. autodoc2-docstring:: simpledali.util.INFO_SERVERID

.. py:data:: INFO_CAPABILITIES
   :canonical: simpledali.util.INFO_CAPABILITIES
   :value: 'Capabilities'

   .. autodoc2-docstring:: simpledali.util.INFO_CAPABILITIES

.. py:data:: INFO_STATUS
   :canonical: simpledali.util.INFO_STATUS
   :value: 'Status'

   .. autodoc2-docstring:: simpledali.util.INFO_STATUS

.. py:data:: INFO_STREAMLIST
   :canonical: simpledali.util.INFO_STREAMLIST
   :value: 'StreamList'

   .. autodoc2-docstring:: simpledali.util.INFO_STREAMLIST

.. py:data:: INFO_STREAM
   :canonical: simpledali.util.INFO_STREAM
   :value: 'Stream'

   .. autodoc2-docstring:: simpledali.util.INFO_STREAM

.. py:function:: prettyPrintInfo(info)
   :canonical: simpledali.util.prettyPrintInfo

   .. autodoc2-docstring:: simpledali.util.prettyPrintInfo

.. py:function:: encodeAuthToken(user_id, expireDelta, writePattern, secretKey)
   :canonical: simpledali.util.encodeAuthToken

   .. autodoc2-docstring:: simpledali.util.encodeAuthToken

.. py:function:: decodeAuthToken(encodedToken, secretKey)
   :canonical: simpledali.util.decodeAuthToken

   .. autodoc2-docstring:: simpledali.util.decodeAuthToken

.. py:function:: timeUntilExpireToken(token)
   :canonical: simpledali.util.timeUntilExpireToken

   .. autodoc2-docstring:: simpledali.util.timeUntilExpireToken
