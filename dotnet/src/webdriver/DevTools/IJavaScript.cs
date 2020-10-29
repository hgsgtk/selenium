// <copyright file="IJavaScript.cs" company="WebDriver Committers">
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
using System.Threading.Tasks;

namespace OpenQA.Selenium.DevTools
{
    /// <summary>
    /// Interface representing the browser's JavaScript execution as referenced by the DevTools Protocol.
    /// </summary>
    public interface IJavaScript
    {
        /// <summary>
        /// Occurs when a JavaScript script binding is called.
        /// </summary>
        event EventHandler<BindingCalledEventArgs> BindingCalled;

        /// <summary>
        /// Occurs when the browser's JavaScript console API is called.
        /// </summary>
        event EventHandler<ConsoleApiCalledEventArgs> ConsoleApiCalled;

        /// <summary>
        /// Occurs when a JavaScript exception is thrown.
        /// </summary>
        event EventHandler<ExceptionThrownEventArgs> ExceptionThrown;

        /// <summary>
        /// Asynchronously enables the Runtime domain in the DevTools Protocol.
        /// </summary>
        /// <returns>A task that represents the asynchronous operation.</returns>
        Task EnableRuntime();

        /// <summary>
        /// Asynchronously disables the Runtime domain in the DevTools Protocol.
        /// </summary>
        /// <returns>A task that represents the asynchronous operation.</returns>
        Task DisableRuntime();

        /// <summary>
        /// Asynchronously enables the Page domain in the DevTools Protocol.
        /// </summary>
        /// <returns>A task that represents the asynchronous operation.</returns>
        Task EnablePage();

        /// <summary>
        /// Asynchronously disables the Page domain in the DevTools Protocol.
        /// </summary>
        /// <returns>A task that represents the asynchronous operation.</returns>
        Task DisablePage();

        /// <summary>
        /// Adds a binding to a specific JavaScript name.
        /// </summary>
        /// <param name="name">The name to which to bind to.</param>
        /// <returns>A task that represents the asynchronous operation.</returns>
        Task AddBinding(string name);

        /// <summary>
        /// Removes a binding from a specific JavaScript name.
        /// </summary>
        /// <param name="name">The name to which to remove the bind from.</param>
        /// <returns>A task that represents the asynchronous operation.</returns>
        Task RemoveBinding(string name);

        /// <summary>
        /// Adds a JavaScript snippet to evaluate when a new document is opened.
        /// </summary>
        /// <param name="script">The script to add to be evaluated when a new document is opened.</param>
        /// <returns>A task that represents the asynchronous operation. The task result contains the internal ID of the script.</returns>
        Task<string> AddScriptToEvaluateOnNewDocument(string script);

        /// <summary>
        /// Removes a JavaScript snippet from evaluate when a new document is opened.
        /// </summary>
        /// <param name="scriptId">The ID of the script to be removed.</param>
        /// <returns>A task that represents the asynchronous operation.</returns>
        Task RemoveScriptToEvaluateOnNewDocument(string scriptId);
    }
}
