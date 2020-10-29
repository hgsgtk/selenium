// <copyright file="V85Log.cs" company="WebDriver Committers">
// Licensed to the Software Freedom Conservancy (SFC) under one
// or more contributor license agreements. See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership. The SFC licenses this file
// to you under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

using System;
using System.Collections.Generic;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using OpenQA.Selenium.DevTools.V86.Log;

namespace OpenQA.Selenium.DevTools.V86
{
    /// <summary>
    /// Class containing the browser's log as referenced by version 86 of the DevTools Protocol.
    /// </summary>
    public class V86Log : ILog
    {
        private LogAdapter adapter;

        /// <summary>
        /// Initializes a new instance of the <see cref="V86Log"/> class.
        /// </summary>
        /// <param name="adapter">The adapter for the Log domain.</param>
        public V86Log(LogAdapter adapter)
        {
            this.adapter = adapter;
            this.adapter.EntryAdded += OnAdapterEntryAdded;
        }

        /// <summary>
        /// Occurs when an entry is added to the browser's log.
        /// </summary>
        public event EventHandler<EntryAddedEventArgs> EntryAdded;

        /// <summary>
        /// Asynchrounously enables manipulation of the browser's log.
        /// </summary>
        /// <returns>A task that represents the asynchronous operation.</returns>
        public async Task Enable()
        {
            await adapter.Enable();
        }

        /// <summary>
        /// Asynchrounously clears the browser's log.
        /// </summary>
        /// <returns>A task that represents the asynchronous operation.</returns>
        public async Task Clear()
        {
            await adapter.Clear();
        }

        private void OnAdapterEntryAdded(object sender, Log.EntryAddedEventArgs e)
        {
            if (this.EntryAdded != null)
            {
                EntryAddedEventArgs propagated = new EntryAddedEventArgs();
                propagated.Entry = new LogEntry();
                propagated.Entry.Kind = e.Entry.Source.ToString();
                propagated.Entry.Message = e.Entry.Text;
                this.EntryAdded(this, propagated);
            }
        }
    }
}
